import pandas as pd

adap_df = pd.read_csv(
    '/Lab_work/data_files/HMDB_sample_files/csv_files/all_spectrum_info_low_res__human_blood_studies_spectra.csv')

csf_df = pd.read_csv('../Lab_work/data_files/HMDB_sample_files/csv_files/csf_metabolites.csv',
                     header=0, index_col=False)
feces_df = pd.read_csv('../Lab_work/data_files/HMDB_sample_files/csv_files/feces_metabolites.csv',
                       header=0, index_col=False)
saliva_df = pd.read_csv('../Lab_work/data_files/HMDB_sample_files/csv_files/saliva_metabolites.csv',
                        header=0, index_col=False)
serum_df = pd.read_csv('../Lab_work/data_files/HMDB_sample_files/csv_files/serum_metabolites.csv',
                       header=0, index_col=False)
sweat_df = pd.read_csv('../Lab_work/data_files/HMDB_sample_files/csv_files/sweat_metabolites.csv',
                       header=0, index_col=False)
urine_df = pd.read_csv('../Lab_work/data_files/HMDB_sample_files/csv_files/urine_metabolites.csv',
                       header=0, index_col=False)

hmdp_df_list = [csf_df, feces_df, saliva_df, serum_df, sweat_df, urine_df]

hmdp_combine_df = pd.concat(hmdp_df_list)

df_common = pd.DataFrame(columns=['index_adap', 'name'])

adap_df_names = adap_df.loc[:, ['Name']]

synonym_list = []
for index, row in hmdp_combine_df.iterrows():
    for i in row['synonyms'].split('|'):
        synonym_list.append(i)

for index, row in adap_df_names.iterrows():
    if row.Name in synonym_list:
        new_row = {'index_adap': index, 'name': row.Name}
        df_common = df_common.append(new_row, ignore_index=True)

df_common.to_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/HMDB_sample_files/blood_common_synonyms_adap_kdb_and_hmdb.csv')