import pandas as pd

df_biomarker_db = pd.read_csv("/Users/ericliao/Downloads/biomarkers.csv")

# df_vip_48 = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
#                        "match_to_nist_files/vip>1/st000058_new_process_signature_0_hour_vs_48_hours.csv")

df_workbench_58 = pd.read_csv("/Users/ericliao/Desktop/df_workbench_edited.csv")
df_new = df_workbench_58[df_workbench_58['Matched'] == 1]

pubchem_id_list = df_biomarker_db['PubChem ID'].tolist()

for i in df_new:
    if i in pubchem_id_list:
        print(i["pubchem_id"])

