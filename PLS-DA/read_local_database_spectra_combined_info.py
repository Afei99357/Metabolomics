import pandas as pd
import numpy as np

df_combine = pd.read_csv("/Users/ericliao/Desktop/similarity_study/study_0609/all_spectrum_info_low_res_combined.csv",
                  header=0, index_col=0)

# get unique submission ID
submission_id_columns_name = df_combine["SubmissionId"].unique()

# create a new dataframe with column name same as submission ID, then store the cluster info
df_clusters = pd.DataFrame(columns=submission_id_columns_name)

# load metadata info as target
df_metadata_target = pd.read_csv(
    "/Users/ericliao/Desktop/similarity_study/study_0609/all_spectrum_info_low_res_metadata.csv",
    header=0, index_col=0)

# get unique cluster id
cluster_list = df_combine["ClusterId"].unique()

for index, row in enumerate(cluster_list):
    row_values = []
    for i in submission_id_columns_name:
        if row in df_combine[df_combine['SubmissionId'] == i]['ClusterId'].values:
            row_values.append(1)
        else:
            row_values.append(0)
    row_values_series = pd.Series(row_values, index=df_clusters.columns)
    df_clusters = df_clusters.append(row_values_series, ignore_index=True)


df1.header()
