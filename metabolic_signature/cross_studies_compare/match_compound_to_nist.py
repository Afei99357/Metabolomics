import pandas as pd
import numpy as np

nist_file_dir = "/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/nist_mspepsearch_return/st000058_new.tsv"
study_vips_dir = "/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000058_new/results/0_hour_vs_2_hours_st000058_vip_greater_0.csv"
output_dir = "/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/match_to_nist_files/top_15_and_vip_greater_than_1/"
output_file_name = "st000058_new_process_signature_0_hour_vs_2_hours.csv"

df_nist = pd.read_csv(nist_file_dir, sep='\t', header=3, index_col=None)
df_nist = df_nist.iloc[0:-2]

df_study_vips = pd.read_csv(study_vips_dir, index_col=None)

df_study_vips = df_study_vips.sort_values("VIP", ascending=False)

df_study_vips_top_15 = df_study_vips.iloc[:15, :]

# df_vip_greater_1 = df_study_vips[df_study_vips["VIP"] >= 1]

column_names = ['position name', 'Library', 'Id', 'Mass', 'Lib MW', 'InLib', 'MF', 'Prob(%)', 'Name', 'Formula', 'CAS',
                'InChIKey', "VIP"]

df_output = pd.DataFrame(columns=column_names)

for index, item in df_study_vips_top_15.iterrows():
    if item['name'] in df_nist['Unknown'].tolist() and item['VIP'] >= 1:
        row_data = df_nist[df_nist['Unknown'] == item['name']]

        new_dict = {'position name': item['name'], 'Library': row_data['Library'], 'Id': row_data['Id'],
                    'Mass': row_data['Mass'], 'Lib MW': row_data['Lib MW'], 'InLib': row_data['InLib'],
                    'MF': row_data['MF'], 'Prob(%)': row_data['Prob(%)'], 'Name': row_data['Name'],
                    'Formula': row_data['Formula'], 'CAS': row_data['CAS'], 'InChIKey': row_data['InChIKey'],
                    'VIP': item['VIP']}

        df_output = df_output.append(new_dict, ignore_index=True)

df_output.to_csv(output_dir + output_file_name)
