import os

import pandas as pd

#### study st000058
group_1_df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/match_to_nist_files/top_15_and_vip_greater_than_1/st000058_new_process_signature_0_hour_vs_2_hours.csv", index_col=0)
group_2_df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/match_to_nist_files/top_15_and_vip_greater_than_1/st000058_new_process_signature_0_hour_vs_4_hours.csv", index_col=0)
group_3_df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/match_to_nist_files/top_15_and_vip_greater_than_1/st000058_new_process_signature_0_hour_vs_8_hours.csv", index_col=0)
group_4_df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/match_to_nist_files/top_15_and_vip_greater_than_1/st000058_new_process_signature_0_hour_vs_12_hours.csv", index_col=0)
group_5_df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/match_to_nist_files/top_15_and_vip_greater_than_1/st000058_new_process_signature_0_hour_vs_24_hours.csv", index_col=0)
group_6_df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/match_to_nist_files/top_15_and_vip_greater_than_1/st000058_new_process_signature_0_hour_vs_48_hours.csv", index_col=0)

list_1 = group_1_df["InChIKey"].tolist()
list_2 = group_2_df["InChIKey"].tolist()
list_3 = group_3_df["InChIKey"].tolist()
list_4 = group_4_df["InChIKey"].tolist()
list_5 = group_5_df["InChIKey"].tolist()
list_6 = group_6_df["InChIKey"].tolist()

common_compounds = list(set.intersection(*map(set, [list_1, list_2, list_3, list_4, list_5, list_6])))

print(common_compounds)

### st000965

# group_1_df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
#                          "match_to_nist_files/top_15_and_vip_greater_than_1/st000965_signature_0_min_vs_30_min.csv", index_col=0)
# group_2_df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
#                          "match_to_nist_files/top_15_and_vip_greater_than_1/st000965_signature_0_min_vs_60_min.csv", index_col=0)
# group_3_df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
#                          "match_to_nist_files/top_15_and_vip_greater_than_1/st000965_signature_0_min_vs_90_min.csv", index_col=0)
#
# list_1 = group_1_df["InChIKey"].tolist()
# list_2 = group_2_df["InChIKey"].tolist()
# list_3 = group_3_df["InChIKey"].tolist()
#
# common_compounds = list(set.intersection(*map(set, [list_1, list_2, list_3])))
#
# print(common_compounds)

# input_directory = "/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/match_to_nist_files/top_15_and_vip_greater_than_1/"

# input_directory = "/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/match_to_nist_files/vip>1/"
# for root, subdirectories, files in os.walk(input_directory):
#     unique_studies_list = set()
#     for file in files:
#         unique_studies_list.add(file.split("_signature",2)[0])
#
#     for m in files:
#         if m == ".DS_Store":
#             continue
#         for n in files:
#             if m.split("_signature", 2)[0] == n.split("_signature", 2)[0] or n == ".DS_Store":
#                 continue
#             else:
#                 df_m = pd.read_csv(os.path.join(root, m), index_col=0)
#                 df_n = pd.read_csv(os.path.join(root, n), index_col=0)
#
#                 list_m = df_m["InChIKey"].tolist()
#                 list_n = df_n["InChIKey"].tolist()
#
#                 common_compounds = list(set.intersection(*map(set, [list_m, list_n])))
#
#                 if len(common_compounds) != 0:
#                     print(m + " and " + n + " has " + str(len(common_compounds)) + " common compounds!")
#                     print(common_compounds)
