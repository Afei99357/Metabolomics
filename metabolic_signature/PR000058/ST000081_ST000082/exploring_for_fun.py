import pandas as pd
import operator
from scipy.stats import f_oneway
from statsmodels.sandbox.stats.multicomp import multipletests
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px

### load data
df_81_82 = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/PR000058/ST000081_ST000082/data/aligned.csv')
df_factor_81_82 = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/PR000058/ST000081_ST000082/data/factors.csv')

for index, item in df_factor_81_82.iterrows():
    item['local_sample_id'] = item['local_sample_id'].strip()

df_height_81_82 = df_81_82.loc[:, [' height' in i for i in df_81_82.columns]]
df_height_81_82 = df_height_81_82.fillna(0)
#
# df_height_transposed_81_82 = df_height_81_82.T
# pvalue_list = []
#
# for index, item in df_height_81_82.iterrows():
#     serum_group = []
#     subcutaenous_group = []
#     visceral_group = []
#     for x in item.index:
#         local_sample_id = x.split(".", 1)[0]
#         tissue_type = df_factor_81_82[df_factor_81_82['local_sample_id'] == local_sample_id]['Tissue type'].values[0]
#         if not pd.isna(item[x]):
#             if operator.contains(tissue_type, "Serum"):
#                 serum_group.append(item[x])
#             if operator.contains(tissue_type, "Subcutaenous Adipose"):
#                 subcutaenous_group.append(item[x])
#             if operator.contains(tissue_type, "Visceral Adipose"):
#                 visceral_group.append(item[x])
#
#     anova_result = f_oneway(serum_group, subcutaenous_group, visceral_group)
#     pvalue_list.append(anova_result.pvalue)
#
# # Compute FDR using Benjamini-Hochberg procedure
# fdrs = multipletests(pvalue_list, method='fdr_bh')[1]

df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
                 "mummichog/mummichog_statistics_st000081_st000082.csv", delimiter="\t")

pvalues = df["p-value"].tolist()

fdrs = multipletests(pvalues, method='fdr_bh')[1]

plt.hist(fdrs, 100)

plt.title("ANOVA test p-values with FDR using BH correction")

plt.show()


scaler = StandardScaler()
scaled_data = scaler.fit_transform(df_height_81_82)
pca = PCA(n_components=3)
pca.fit(scaled_data)
X_pca = pca.transform(scaled_data)

total_var = pca.explained_variance_ratio_.sum() * 100

labels = {
        str(i): f"PC {i + 1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }

x = X_pca[:, 0]
y = X_pca[:, 1]
z = X_pca[:, 2]

# plot 3d scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z)

plt.show()

    # .scatter_3d(scaled_data, x=0, y=1, z=2, title=f'Total Explained Variance: {total_var:.2f}%',
    #                            labels=labels)
# fig_3D.show()



