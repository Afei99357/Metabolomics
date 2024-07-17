import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.cluster import fowlkes_mallows_score

#
df = pd.read_csv(
    "/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/adap_kdb_algorithm_comparison/"
    "adap_kdb_high_res_similarity_score_result_with_different_tolerance/thresholed_0.6_match_results.csv")

df = df[['QuerySpectrumId', 'MatchSpectrumId', 'Score']]

# annotated spectra
high_res_df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/"
                          "adap_kdb_algorithm_comparison/high_resolution_spectra_informtion/high_res_gas_annotated_specra.csv")

df_merge = pd.merge(df, high_res_df, how='inner', left_on="QuerySpectrumId", right_on="Id")

df_merge = pd.merge(df_merge, high_res_df, how='inner', left_on="MatchSpectrumId", right_on="Id", suffixes=('Query', 'Match'))

# df_merge.to_csv('/Users/ericliao/Downloads/merge.csv')


matrix_df = pd.DataFrame(columns=high_res_df.Id, index=high_res_df.Id)

for index, item in df_merge.iterrows():
    matrix_df.at[item[0], item[1]] = 1 - item[2]
    # matrix_df.at[item[1], item[0]] = 1 - item[2]

matrix_df = matrix_df.fillna(1)

clustering = AgglomerativeClustering(n_clusters=None,
                                     affinity='precomputed',
                                     compute_full_tree=True,
                                     linkage='complete',
                                     distance_threshold=0.4).fit(matrix_df.to_numpy())

########## Fowlkes Mallows Score #############
unique_name_list = high_res_df['Name'].unique()

unique_name_dict = {k: v for v, k in enumerate(unique_name_list)}

df_true_name_matrix = high_res_df[['Name']]

for index, item in df_true_name_matrix.iterrows():
    df_true_name_matrix.at[index, 'Name'] = unique_name_dict[item[0]]


fowlkes_mallows_score = fowlkes_mallows_score(df_true_name_matrix['Name'].values,
                                              clustering.labels_)
##############################################

print(fowlkes_mallows_score)