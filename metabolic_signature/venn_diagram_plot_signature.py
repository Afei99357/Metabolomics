import pandas as pd
import matplotlib.pyplot as plt
from venn import pseudovenn
from venn import venn


df_2hour = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
                       "match_to_nist_files/vip>1/st000058_new_process_signature_0_hour_vs_2_hours.csv")
df_4hour = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
                       "match_to_nist_files/vip>1/st000058_new_process_signature_0_hour_vs_4_hours.csv")
df_8hour = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
                       "match_to_nist_files/vip>1/st000058_new_process_signature_0_hour_vs_8_hours.csv")
df_12hour = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
                       "match_to_nist_files/vip>1/st000058_new_process_signature_0_hour_vs_12_hours.csv")
df_24hour = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
                       "match_to_nist_files/vip>1/st000058_new_process_signature_0_hour_vs_24_hours.csv")
df_48hour = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
                       "match_to_nist_files/vip>1/st000058_new_process_signature_0_hour_vs_48_hours.csv")

name_2hour = set(df_2hour['position name'].tolist())
name_4hour = set(df_4hour['position name'].tolist())
name_8hour = set(df_8hour['position name'].tolist())
name_12hour = set(df_12hour['position name'].tolist())
name_24hour = set(df_24hour['position name'].tolist())
name_48hour = set(df_48hour['position name'].tolist())

labels = ["2 hours", "4 hours", "8 hours", "12 hours", "24 hours", "48 hours"]

sets = {labels[0]: name_2hour,
        labels[1]: name_4hour,
        labels[2]: name_8hour,
        labels[3]: name_12hour,
        labels[4]: name_24hour,
        labels[5]: name_48hour}

fig, ax = plt.subplots(1, figsize=(10, 10))
a = venn(sets, ax=ax)
plt.legend(labels[:], ncol=6)

plt.show()

for i in name_48hour:
    if i not in name_2hour:
        if i not in name_4hour:
            if i not in name_8hour:
                if i not in name_12hour:
                    if i not in name_24hour:
                        print(i)


