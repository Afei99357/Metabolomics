import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import special
from sklearn.cross_decomposition import PLSRegression
import sklearn
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

plt.style.use('ggplot')
fig = plt.figure(1, figsize=(10, 7))
plt.clf()

########################## local data ########################
df_combine = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/data_files/all_spectrum_info_high_res_with_name_combined.csv",
                         header=0, index_col=0)

# # get unique submission ID
# submission_id_columns_name = df_combine["SubmissionId"].unique()
#
# # get unique cluster id
# cluster_list = df_combine["ClusterId"].unique()
#
# np.savetxt('/Users/ericliao/PycharmProjects/Phd_Class/data_files/unique_cluster_list_high_res.csv', cluster_list, delimiter=",")
#
# # create a new dataframe with column name same as submission ID, then store the cluster info
# df_clusters = pd.DataFrame(columns=submission_id_columns_name)
#
# # to get the cluster information of each submission
# for index, row in enumerate(cluster_list):
#     row_values = []
#     for i in submission_id_columns_name:
#         if row in df_combine[df_combine['SubmissionId'] == i]['ClusterId'].values:
#             row_values.append(1)
#         else:
#             row_values.append(0)
#     row_values_series = pd.Series(row_values, index=df_clusters.columns)
#     df_clusters = df_clusters.append(row_values_series, ignore_index=True)
#
#
# df_clusters.to_csv("/Users/ericliao/PycharmProjects/Phd_Class/data_files/local_cluster_infor_high_res.csv")

# load metadata info as target
df_metadata_target = pd.read_csv(
    "/Users/ericliao/PycharmProjects/Phd_Class/data_files/all_spectrum_info_high_res_metadata.csv",
    header=0)

### choose only the species is human
# df_metadata_target = df_metadata_target[(df_metadata_target['species'] == 'human') &
#                                         (df_metadata_target["disease"] == "cancer")]
df_metadata_target = df_metadata_target[df_metadata_target['species'] == 'human']
# df_metadata_target = df_metadata_target.drop([6, 41, 37, 38, 21], axis=0)

# ### choose only the species is human and mouse
# human_mouse_array = ["human", "mouse"]
# df_metadata_target = df_metadata_target.loc[df_metadata_target['species'].isin(human_mouse_array)]
# df_metadata_target = df_metadata_target.drop([6, 41, 37, 38, 21], axis=0)

# set up target
# target = df_metadata_target['sample source'].values
# target_3d = target
# target_unique = df_metadata_target['sample source'].unique()
#
# for index, row in enumerate(target_3d):
#     if row == 'cultured cells':
#         target_3d[index] = 0
#     else:
#         target_3d[index] = 1

# set dummy variable accoring one column value as target
target_3d = pd.get_dummies(df_metadata_target[['sample source']]).values

target_sample_color = [0, 0, 0, 0, 1, 0, 0, 2, 2]

# ## set up target on diseases
# target = df_metadata_target['disease'].values
# target_3d = target
# for index, row in enumerate(target):
#     if row == 'cancer':
#         target_3d[index] = 0
#     else:
#         target_3d[index] = 1

### set target according to how many types
# n = 0
# for index, row in enumerate(target_unique):
#     for index2, row2 in enumerate(target):
#         if row2 == row:
#             target[index2] = n
#     n = n + 1

df_clusters_original = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/data_files/local_cluster_infor_high_res.csv",
                          header=0, index_col=0)

# df_clusters = df_clusters.drop(['119', '164', '101'], axis=1)
# df_clusters = df_clusters.drop(df_clusters.index[7226])

### only human
df_clusters_human = df_clusters_original[['134', '135', '136', '137', '140', '143', '144', '145', '146']]

# ### only cancer
# df_clusters_human_mouse = df_clusters[['96', '98', '100', '107', '126', '128', '165', '166', '167', '168', '169',
#                                        '174', '184']]

# ### only mouse and human
# df_clusters_human_mouse = df_clusters[['96', '97', '98', '100', '104', '105', '106', '107', '108', '109', '111',
#                                        '113', '114', '117', '120', '121', '126', '127', '128',
#                                        '163', '165', '166', '167', '168', '169', '171', '174', '175', '176',
#                                        '177', '178', '179', '180', '181', '182', '184', '185', '186', '187', '188']]

# df_clusters_human_mouse.to_csv('/Users/yliao13/Desktop/pca/local_cluster_info_human_mouse.csv')

##### transpose the matrix
df_clusters = df_clusters_human.values
df_clusters = df_clusters.T

# ############preprocess data using mean center
# df = (df - df.mean(axis=1, keepdims=True)) / df.std(axis=1, keepdims=True)
scaler = StandardScaler()
df_clusters = pd.DataFrame(scaler.fit_transform(df_clusters))
df_clusters_values = df_clusters.values

#### get vips score #######
def vip(model):
    t = model.x_scores_
    w = model.x_weights_
    q = model.y_loadings_
    p, h = w.shape
    vips = np.zeros((p,))
    s = np.diag(t.T @ t @ q.T @ q).reshape(h, -1)
    total_s = np.sum(s)
    for i in range(p):
        weight = np.array([(w[i, j] / np.linalg.norm(w[:, j])) ** 2 for j in range(h)])
        vips[i] = np.sqrt(p * (s.T @ weight) / total_s)
    return vips
#########################

####### leave one out cross validation #######################
# calculate R2 values and store in a list
r2_list = []

# # create empty numpy array to store test values and predict values
test_values = np.zeros((9, 3))
predicted_values = np.zeros((9, 3))

for i in range(len(df_clusters_values)):
    train_selection = [j for j in range(len(df_clusters_values)) if i != j]
    test_selection = [i]
    # np.random.seed(0)
    # np.random.shuffle(selection)

    # train_selection = selection[:8]
    # test_selection = selection[8:]

    train_x = df_clusters_values[train_selection, :]
    train_y = target_3d[train_selection]
    # train_color = target_species_color[train_selection]

    test_x = df_clusters_values[test_selection, :]
    test_y = target_3d[test_selection]

    plsr = PLSRegression(n_components=2, scale=False)
    plsr.fit(train_x, train_y)

    predict_y = plsr.predict(test_x)

    test_values[i] = test_y
    predicted_values[i] = predict_y

    soft_max_y = special.softmax(predict_y)

    # print(np.argmax(test_y), np.argmax(predict_y))
    r2_list.append(metrics.r2_score(test_y.flatten(), predict_y.flatten()))

    ## calculate vip score
    vip_value = vip(plsr)

    index = np.argsort(vip_value)[-10:]

    # print(index, vip_value[index])

test_values = np.array(test_values)
predicted_values = np.array(predicted_values)

###############################################################
# ##plot for R2
# plt.scatter(test_values[:, 0], predicted_values[:, 0])
# plt.scatter(test_values[:, 1], predicted_values[:, 1])

r2_1 = sklearn.metrics.r2_score(test_values[:, 0], predicted_values[:, 0])
r2_2 = sklearn.metrics.r2_score(test_values[:, 1], predicted_values[:, 1])
r2_3 = sklearn.metrics.r2_score(test_values[:, 2], predicted_values[:, 2])

print(r2_1, r2_2, r2_3)

# ####### PLS-DA########
plsr = PLSRegression(n_components=2, scale=False)

plsr.fit(df_clusters_values, target_3d)
vip_value = vip(plsr)

index = np.argsort(vip_value)[-10:]
print(index)

# socres: The scores describe the position of each sample in each determined latent variable (LV)
scores = pd.DataFrame(plsr.x_scores_).to_numpy()

# ###### 2D plot for PLS-DA #######
# plot = plt.scatter(scores[:, 0], scores[:, 1], c=target, edgecolors='none', alpha=0.7,
#             cmap=plt.cm.get_cmap('tab20', 2), s=70)
#
# plt.xlabel("Scores on LV 1")
# plt.ylabel("Scores on LV 2")
# classes = ["human", "non-human"]
# plt.legend(handles=plot.legend_elements()[0], labels=classes)
# plt.clim(0, 2)
# plt.colorbar()
#################################

# ####### plot study id as label on each dot######
scores_df = pd.DataFrame(plsr.x_scores_)
scores_df.index = df_clusters_human.columns
ax = plt.scatter(scores_df[0], scores_df[1], s=70, alpha=0.7, c=target_sample_color, cmap=plt.cm.get_cmap('tab20', 3))
plt.xlabel("Scores on LV 1")
plt.ylabel("Scores on LV 2")
classes = ["cultured cells", 'blood', 'breast']
plt.legend(handles=ax.legend_elements()[0], labels=classes)
for n, (x, y) in enumerate(scores_df.values):
    label = scores_df.index.values[n]
    plt.text(x, y, label)
###############################################


# ####### 3D plot for PLS-DA #######
# ax = fig.add_subplot(111, projection='3d')
#
# ax.scatter(scores[:, 0], scores[:, 1], scores[:, 2], c=target_3d, cmap=plt.cm.get_cmap('tab20', 16), s=70)
#
# ax.set_xlabel("Score on LV1")
# ax.set_ylabel("Score on LV2")
# ax.set_zlabel("Score on LV3")
# ###############################

plt.show()
