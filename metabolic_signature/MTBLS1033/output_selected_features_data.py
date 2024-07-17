import pandas as pd

df_features = pd.read_csv(
    "/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/MTBLS1033/POS/"
    "with_feature_selection/train_data_top10_matched_vips_aligned.csv",
    index_col=0,
)

df_test_data = pd.read_csv(
    "/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/MTBLS1033/POS/"
    "with_feature_selection/test_data_20_percent.csv",
    index_col=0,
)


feature_number = df_features["Unnamed: 0.1"].tolist()

df_new = df_test_data.T.iloc[feature_number]

df_final = df_new.T

df_final["target"] = df_test_data.T.loc["target"].tolist()

df_final.to_csv(
    "/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/MTBLS1033/POS/with_feature_selection/"
    "testing_data_after_selected_feature_aligned_data.csv"
)
