import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

df_origin = pd.read_csv("/Users/yliao13/Desktop/pca/LipidsWG_QEHF_POS_processed_with_mz.csv", header=0)
df = df_origin.loc[:, 'Brain1': 'Plasma13']
# target = np.array(["Brain", "Brain", "Brain", "Heart", "Heart", "Heart", "Liver", "Liver",
#           "Liver", "Muscle", "Muscle", "Muscle", "Plasma", "Plasma", "Plasma"])

# 0-brain, 1-heart, 2-liver, 3-muscle, 4-plasma
target = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])

###### 2d pca plot #######
#transpose array
X = df.to_numpy().T
fig = plt.figure(1, figsize=(10, 7))
plt.clf()

pca = PCA(n_components=2)
Y = pca.fit_transform(X)

plt.scatter(Y[:, 0], Y[:, 1], c=target, edgecolors='none', alpha=0.5, cmap=plt.cm.get_cmap('Set2_r', 5), s=70)

# sorting scires by each column separately
weight_sort_array_1 = np.argsort(pca.components_[0])
weight_sort_array_2 = np.argsort(pca.components_[1])

# get top 10 and bottom 10 from each column
weight_10_max_1 = weight_sort_array_1[0: 10]
weight_10_min_1 = weight_sort_array_1[-10:]

weight_10_max_2 = weight_sort_array_2[0: 10]
weight_10_min_2 = weight_sort_array_2[-10:]

############# to find the top 10, bottom 10 weighted of LV1 AND LV2 features##################
df_new = pd.DataFrame(columns=["Index", 'Weight', 'Metabolite Name', 'Average Mz', 'Average Retention Time', 'Brain1',
                               'Brain2', 'Brain3', 'Heart1', 'Heart2', 'Heart3', 'Liver1', 'Liver2', 'Liver3',
                               'Muscle1',
                               'Muscle2', 'Muscle3', 'Plasma1', 'Plasma2', 'Plasma3'])

df_1 = df_origin.iloc[[i for i in weight_10_max_1], :]
df_2 = df_origin.iloc[[i for i in weight_10_min_1], :]
df_3 = df_origin.iloc[[i for i in weight_10_max_2], :]
df_4 = df_origin.iloc[[i for i in weight_10_min_2], :]

for index, row in df_1.iterrows():
    df_1.loc[index, 'Weight'] = pca.components_[0][row['Index']]
    print(row['Weight'])

for index, row in df_2.iterrows():
    df_2.loc[index, 'Weight'] = pca.components_[0][row['Index']]
    print(row['Weight'])

for index, row in df_3.iterrows():
    df_3.loc[index, 'Weight'] = pca.components_[0][row['Index']]
    print(row['Weight'])

for index, row in df_4.iterrows():
    df_4.loc[index, 'Weight'] = pca.components_[0][row['Index']]
    print(row['Weight'])

df_1.to_csv("/Users/yliao13/Desktop/pca/pca_top_10_component_1.csv", index=False)
df_2.to_csv("/Users/yliao13/Desktop/pca/pca_bottom_10_component_1.csv", index=False)
df_3.to_csv("/Users/yliao13/Desktop/pca/pca_top_10_component_2.csv", index=False)
df_4.to_csv("/Users/yliao13/Desktop/pca/pca_bottom_10_component_2.csv", index=False)
######################################

plt.title("Total {: .3}".format(sum(pca.explained_variance_ratio_ * 100)) + "% of samples will be explained")
plt.xlabel("PC1: {: .3}".format(pca.explained_variance_ratio_[0] * 100) + "%")
plt.ylabel("PC2: {: .3}".format(pca.explained_variance_ratio_[1] * 100) + '%')
plt.clim(0, 5)
plt.colorbar()



# # ######### 3d pca plot ###########
# # transpose for the data
# X = df.T
#
# fig = plt.figure()
# pca = PCA(n_components=3)
# pca.fit_transform(X)
#
# # Store results of PCA in a data frame
# result = pd.DataFrame(pca.transform(X), columns=['PCA%i' % i for i in range(3)], index=X.index)
#
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(result['PCA0'], result['PCA1'], result['PCA2'], c=target, cmap='Set2_r', s=70)
#
# ax.set_xlabel("PC1: {:.3}".format(pca.explained_variance_ratio_[0] * 100) + '%')
# ax.set_ylabel("PC2: {:.3}".format(pca.explained_variance_ratio_[1] * 100) + '%')
# ax.set_zlabel("PC3: {:.3}".format(pca.explained_variance_ratio_[2] * 100) + '%')
# ax.set_title("Total {: .3}".format(sum(pca.explained_variance_ratio_ * 100)) + "% of samples will be explained")


plt.show()