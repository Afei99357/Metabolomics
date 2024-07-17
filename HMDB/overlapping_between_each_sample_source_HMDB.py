import pandas as pd
from venn import venn
import matplotlib.pyplot as plt

df_csf = pd.read_csv("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/HMDB_sample_files/csv_files/csf_metabolites.csv")

df_feces = pd.read_csv("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/HMDB_sample_files/csv_files/feces_metabolites.csv")

df_saliva = pd.read_csv("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/HMDB_sample_files/csv_files/saliva_metabolites.csv")

df_serum = pd.read_csv("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/HMDB_sample_files/csv_files/serum_metabolites.csv")

df_sweat = pd.read_csv("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/HMDB_sample_files/csv_files/sweat_metabolites.csv")

df_urine = pd.read_csv("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/HMDB_sample_files/csv_files/urine_metabolites.csv")

csf_set = set(df_csf["accession"].tolist())
feces_set = set(df_feces["accession"].tolist())
saliva_set = set(df_saliva["accession"].tolist())
serum_set = set(df_serum["accession"].tolist())
sweat_set = set(df_sweat["accession"].tolist())
urine_set = set(df_urine["accession"].tolist())

labels = ["csf", "feces", "saliva", "serum", "sweat", "urine"]

sets = {
    labels[0]: csf_set,
    labels[1]: feces_set,
    labels[2]: saliva_set,
    labels[3]: serum_set,
    labels[4]: sweat_set,
    labels[5]: urine_set
        }
fig, ax = plt.subplots(1, figsize=(10, 10))
venn(sets, ax=ax)
plt.legend(labels[:], ncol=2)
plt.show()