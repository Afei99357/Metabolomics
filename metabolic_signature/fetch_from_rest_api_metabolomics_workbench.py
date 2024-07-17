import requests
import pandas as pd

api_url = "https://www.metabolomicsworkbench.org/rest/study/study_id/ST000058/metabolites/"

response = requests.get(api_url)

metabolites_dict = response.json()

output_df = pd.DataFrame(column=["name", "pubchem_id"])

for i in metabolites_dict:
    row = {"name": metabolites_dict[i]["metabolite_name"], "pubchem_id": metabolites_dict[i]['pubchem_id']}
    output_df = output_df.append(row, ignore_index=True)

output_df.to_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/metabolomics_workbench_metabolites_of_study/st000058_metabolites.csv")

