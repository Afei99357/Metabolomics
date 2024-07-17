import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn import model_selection
import sklearn
from scipy import special
from sklearn.preprocessing import StandardScaler

plt.style.use('ggplot')
fig = plt.figure(1, figsize=(10, 7))
plt.clf()

################### Data from consortium ################
df_origin = pd.read_csv('/Users/yliao13/phd_class_code/Lab_work/data_files/consortium_data/LipidsWG_QEHF_POS_processed_with_mz.csv', header=0)
df = df_origin.loc[:, 'Brain1': 'Plasma13'].values
df = df.T

# #preprocess data using mean center
# df = (df - df.mean(axis=1, keepdims=True)) / df.std(axis=1, keepdims=True)

scaler = StandardScaler()
df = pd.DataFrame(scaler.fit_transform(df)).values

# pd.DataFrame(df).to_csv("/Users/ericliao/Desktop/similarity_study/consortium_Data/LipidsWG_QEHF_POS_processed_with_mz_preprocessing.csv")

# ####plot the dataset
# df.plot(kind='line', legend=False, figsize=(12, 4))

# ###### [1,0,0,0,0]-brain, [0,1,0,0,0]-heart, [0,0,1,0,0]-liver, [0,0,0,1,0]-muscle, [0,0,0,0,1]-plasma
target_sample_source = np.array([[1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0],
                                 [0, 1, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 0, 0, 0],
                                 [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0],
                                 [0, 0, 0, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 0],
                                 [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1]])
target_sample_source_color = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])

# ###### [0,1]-human, [1,0]-non-human
target_human_non_human = np.array([[0, 1], [0, 1], [0, 1],
                                   [0, 1], [0, 1], [0, 1],
                                   [0, 1], [0, 1], [0, 1],
                                   [1, 0], [1, 0], [1, 0],
                                   [1, 0], [1, 0], [1, 0]])
target_human_non_human_color = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

# ###### [1,0,0]-pig, [0,1,0]-cow, [0,0,1]-human
target_species = np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0],
                           [0, 1, 0], [0, 1, 0], [0, 1, 0],
                           [0, 1, 0], [0, 1, 0], [0, 1, 0],
                           [0, 0, 1], [0, 0, 1], [0, 0, 1],
                           [0, 0, 1], [0, 0, 1], [0, 0, 1]])

target_species_color = [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]

###########################################################

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

# ######## k-fold cross-validation for PLS-DA model############
selection = [i for i in range(len(df))]

####### leave one out cross validation #######################
# calculate R2 values and store in a list
r2_list = []

# # create empty numpy array to store test values and predict values
test_values = np.zeros((15, 3))
predicted_values = np.zeros((15, 3))

for i in range(len(df)):
    train_selection = [j for j in range(len(df)) if i != j]
    test_selection = [i]
    # np.random.seed(0)
    # np.random.shuffle(selection)

    # train_selection = selection[:8]
    # test_selection = selection[8:]

    train_x = df[train_selection, :]
    train_y = target_species[train_selection]
    # train_color = target_species_color[train_selection]

    test_x = df[test_selection, :]
    test_y = target_species[test_selection]

    plsr = PLSRegression(n_components=2, scale=False)
    plsr.fit(train_x, train_y)

    predict_y = plsr.predict(test_x)

    test_values[i] = test_y
    predicted_values[i] = predict_y

    soft_max_y = special.softmax(predict_y)

    # print(np.argmax(test_y), np.argmax(predict_y))
    # r2_list.append(sklearn.metrics.r2_score(test_y.flatten(), predict_y.flatten()))

    ## calculate vip score
    vip_value = vip(plsr)

    index = np.argsort(vip_value)[-10:]

    # print(index, vip_value[index])

test_values = np.array(test_values)
predicted_values = np.array(predicted_values)

# #find the biggest number in a row, and convert it to 1, and the rest convert to 0
# def convert_value_to_binary(matrix_to_convert):
#     index_matrix = 0
#     for i in matrix_to_convert:
#         column_number = i.size
#         # find the biggest value
#         max_value = 0
#         max_value_index = 0
#         for m in range(column_number):
#             if matrix_to_convert[index_matrix][m] >= max_value:
#                 max_value = matrix_to_convert[index_matrix][m]
#                 max_value_index = m
#             matrix_to_convert[index_matrix][max_value_index] = 1
#         for m in range(column_number):
#             if m != max_value_index:
#                 matrix_to_convert[index_matrix][m] = 0
#         index_matrix += 1
#     return matrix_to_convert

# test_values = convert_value_to_binary(test_values)
# predicted_values = convert_value_to_binary(predicted_values)

###############################################################
# ##plot for R2
# plot = plt.scatter(test_values[:, 0], predicted_values[:, 0], c=target_human_non_human_color)
# plot = plt.scatter(test_values[:, 1], predicted_values[:, 1], c=target_human_non_human_color)
# # plt.scatter(test_values[:, 2], predicted_values[:, 2])
# classes = ["human", "non-human"]
# plt.legend(handles=plot.legend_elements()[0], labels=classes)

r2_1 = sklearn.metrics.r2_score(test_values[:, 0], predicted_values[:, 0])
r2_2 = sklearn.metrics.r2_score(test_values[:, 1], predicted_values[:, 1])
r2_3 = sklearn.metrics.r2_score(test_values[:, 2], predicted_values[:, 2])
# r2_4 = sklearn.metrics.r2_score(test_values[:, 3], predicted_values[:, 3])
# r2_5 = sklearn.metrics.r2_score(test_values[:, 4], predicted_values[:, 4])

print(r2_1, r2_2, r2_3)
####################################################
# print out the mean value of R2 value
# print(np.mean(r2_list))

###########  deprecated ##########
# X_train, X_test, Y_train, Y_test = model_selection.train_test_split(df, target, test_size=0.5, random_state=100)
# kfold = model_selection.KFold(n_splits=5, random_state=100, shuffle=True)
# plsr = PLSRegression(n_components=2, scale=False)
# # plsr.fit(X_train, Y_train)
# result = model_selection.cross_validate(plsr, df, target, cv=kfold)
# print(result["test_score"])
# # print(plsr.y_scores_)
# # print("Accuracy: %.2f%%" % (result.mean()*100.0))
# print(result)
# #############################################

####### PLS-DA ########
plsr = PLSRegression(n_components=2, scale=False)
plsr.fit(df, target_species)
# calculate vip score
vip_value = vip(plsr)

index = np.argsort(vip_value)[-10:]
#
# predict_y = plsr.predict(test_x)
#
# print(test_y)
# print(predict_y)
# # print(plsr.x_scores_)
#
# print(plsr.x_weights_)
# print(plsr.x_weights_.max(axis=0))
# print(plsr.x_weights_.min(axis=0))

# print(np.linalg.norm(plsr.x_weights_))
# print(np.dot(df.T, target_color)/np.linalg.norm(np.dot(df.T, target_color)))

# ############# to find the top 10, bottom 10 weighted of LV1 AND LV2 features##################
# # sorting scires by each column separately
# weight_sort_array_1 = np.argsort(plsr.x_weights_[:, 0])
# weight_sort_array_2 = np.argsort(plsr.x_weights_[:, 1])
#
# # get top 10 and bottom 10 from each column
# weight_10_max_1 = weight_sort_array_1[0: 10]
# weight_10_min_1 = weight_sort_array_1[-10:]
#
# weight_10_max_2 = weight_sort_array_2[0: 10]
# weight_10_min_2 = weight_sort_array_2[-10:]
# df_new = pd.DataFrame(columns=["Index", 'Weight', 'Metabolite Name', 'Average Mz', 'Average Retention Time', 'Brain1',
#                                'Brain2', 'Brain3', 'Heart1', 'Heart2', 'Heart3', 'Liver1', 'Liver2', 'Liver3',
#                                'Muscle1',
#                                'Muscle2', 'Muscle3', 'Plasma1', 'Plasma2', 'Plasma3'])
#
# df_1 = df_origin.iloc[[i for i in w eight_10_max_1], :]
# df_2 = df_origin.iloc[[i for i in weight_10_min_1], :]
# df_3 = df_origin.iloc[[i for i in weight_10_max_2], :]
# df_4 = df_origin.iloc[[i for i in weight_10_min_2], :]
#
# for index, row in df_1.iterrows():
#     df_1.loc[index, 'Weight'] = plsr.x_weights_[:, 0][row['Index']]
#     print(row['Weight'])
#
# for index, row in df_2.iterrows():
#     df_2.loc[index, 'Weight'] = plsr.x_weights_[:, 0][row['Index']]
#     print(row['Weight'])
#
# for index, row in df_3.iterrows():
#     df_3.loc[index, 'Weight'] = plsr.x_weights_[:, 0][row['Index']]
#     print(row['Weight'])
#
# for index, row in df_4.iterrows():
#     df_4.loc[index, 'Weight'] = plsr.x_weights_[:, 0][row['Index']]
#     print(row['Weight'])
#
# df_1.to_csv("/Users/yliao13/Desktop/pca/top_10_column_1.csv", index=False)
# df_2.to_csv("/Users/yliao13/Desktop/pca/bottom_10_column_1.csv", index=False)
# df_3.to_csv("/Users/yliao13/Desktop/pca/top_10_column_2.csv", index=False)
# df_4.to_csv("/Users/yliao13/Desktop/pca/bottom_10_column_2.csv", index=False)
# print("top 10 score for first column are: " + str(weight_10_max_1))
# print("bottom 10 score for first column are: " + str(weight_10_min_1))
# print("top 10 score for second column are: " + str(weight_10_max_2))
# print("bottom 10 score for second column are: " + str(weight_10_min_2))
# #####################################

############# to find the top 10 vips lipids data##################
df_new = pd.DataFrame(columns=["Index", 'Vip', 'Metabolite Name', 'Average Mz', 'Average Retention Time', 'Brain1',
                               'Brain2', 'Brain3', 'Heart1', 'Heart2', 'Heart3', 'Liver1', 'Liver2', 'Liver3',
                               'Muscle1',
                               'Muscle2', 'Muscle3', 'Plasma1', 'Plasma2', 'Plasma3'])

df_output = df_origin.iloc[[i for i in index], :]

for index, row in df_output.iterrows():
    df_output.loc[index, 'Vip'] = vip_value[row['Index']]

# df_output.to_csv("/Users/yliao13/Desktop/pca/new_plots/top_10_vips_lipids_5_groups.csv", index=False)

#####################################

# ##### scores: The scores describe the position of each sample in each determined latent variable (LV)
scores = pd.DataFrame(plsr.x_scores_).to_numpy()

##### 2D plot for PLS-DA #######
plot = plt.scatter(scores[:, 0], scores[:, 1], c=target_species_color, edgecolors='none', alpha=0.7,
                   cmap=plt.cm.get_cmap('tab20', 3), s=70)

plt.xlabel("Scores on LV 1")
plt.ylabel("Scores on LV 2")
classes = ["pig", "cow", "human"]
plt.legend(handles=plot.legend_elements()[0], labels=classes)
plt.clim(0, 3)
plt.colorbar()
###############################

# ####### plot study id as label on each dot######
# scores_df = pd.DataFrame(plsr.x_scores_)
# scores_df.index = df_clusters.columns
# ax = scores_df.plot(x=0, y=1, kind='scatter', s=50, alpha=0.7, c=target,cmap=plt.cm.get_cmap('Set2_r', 2), figsize=(6, 6))
# ax.set_xlabel("Scores on LV 1")
# ax.set_ylabel("Scores on LV 2")
# for n, (x, y) in enumerate(scores_df.values):
#     label = scores_df.index.values[n]
#     ax.text(x, y, label)
# ###############################################


# ####### 3D plot for PLS-DA #######
# ax = fig.add_subplot(111, projection='3d')
#
# ax.scatter(scores[:, 0], scores[:, 1], scores[:, 2], c=target, cmap=plt.cm.get_cmap('Set2_r', 16), s=70)
#
# ax.set_xlabel("Score on LV1")
# ax.set_ylabel("Score on LV2")
# ax.set_zlabel("Score on LV3")
# ###############################

plt.show()
