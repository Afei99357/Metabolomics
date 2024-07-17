import pandas as pd

df_1 = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/data_files/all_spectra_info_high_res_metadata_with_name.csv", delimiter=",")
df_2 = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/data_files/all_spectrum_info_high_res_metadata.csv")
# df.index = [x for x in range(1, len(df.values)+1)]
#
# df_2 = pd.read_csv("/Users/yliao13/Desktop/prescreen_origin_search_comparison/time_cost.csv", delimiter=",")
# df_2.index = [x for x in range(1, len(df_2.values)+1)]

# df_new = pd.DataFrame(df['SubmissionId'].unique())
#
# df_new.to_csv("/Users/ericliao/Desktop/similarity_study/study_0609/unique_submissionId.csv", index=False, sep=',')
df_combine = pd.merge(df_1, df_2, on=["SubmissionId"], how="left")

df_combine.to_csv('/Users/ericliao/PycharmProjects/Phd_Class/data_files/all_spectrum_info_high_res_with_name_combined.csv')
