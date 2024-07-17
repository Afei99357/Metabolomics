import pandas as pd

df_original = pd.read_csv("/Users/ericliao/PycharmProjects/phd_class_code/Lab_work/data_files/adap_kdb_algorithm_comparison/study_1110_spectra/original.csv", header=0)
df_prescreen = pd.read_csv("/Users/ericliao/PycharmProjects/phd_class_code/Lab_work/data_files/adap_kdb_algorithm_comparison/study_1110_spectra/prescreen_threshold_500_query_8_to_library_15_matches.csv", header=0)

df_original = df_original.dropna()
df_prescreen = df_prescreen.dropna()

df_combine = pd.merge(df_original, df_prescreen, on=["Query Spectrum ID", "Match Spectrum ID"], how="outer")

df_combine.rename(columns={"Score_x": "Score Original", "Score_y": "Score Prescreen"}, inplace=True)

df_combine.to_csv("/Users/ericliao/PycharmProjects/phd_class_code/Lab_work/data_files/adap_kdb_algorithm_comparison/study_1110_spectra/time/8_15/prescreen_threshold_500_query_8_to_library_15_matches_combine.csv")
