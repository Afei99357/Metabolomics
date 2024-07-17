import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.cross_decomposition import PLSRegression
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

df_origin = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/consortium_lipid_data_new/'
                        'GaTech.csv', header=0, index_col=False)

df_origin_all = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/consortium_lipid_data_new/'
                            'Umich.csv', header=0, index_col=False)

# df_origin = df_origin_all.loc[:, '01_Brain': '03_Plasma01']

## transpose df
# df_origin_intensity = df_origin.T
df_origin_intensity = df_origin_all.T

## preprocessing data
scaler = StandardScaler()
df = pd.DataFrame(scaler.fit_transform(df_origin_intensity)).values

# ###### create target and target color for plot######
# target = np.zeros(shape=(15, 5))
# target_color = []
# target_index = 0
# for i in df_origin_all.columns:
#     if 'Brain' in str(i):
#         target[target_index] = [1, 0, 0, 0, 0]
#         target_color.append(0)
#     if 'Heart' in str(i):
#         target[target_index] = [0, 1, 0, 0, 0]
#         target_color.append(1)
#     if 'Liver' in str(i):
#         target[target_index] = [0, 0, 1, 0, 0]
#         target_color.append(2)
#     if 'Muscle' in str(i):
#         target[target_index] = [0, 0, 0, 1, 0]
#         target_color.append(3)
#     if 'Plasma1' in str(i):
#         target[target_index] = [0, 0, 0, 0, 1]
#         target_color.append(4)
#     target_index += 1

###### create target and target color for plot######
target = np.zeros(shape=(15, 3))
target_color = []
target_index = 0
for i in df_origin_all.columns:
    if str(i).endswith('BRAIN'):
        target[target_index] = [1, 0, 0]  # Pig
        target_color.append(0)
    if str(i).endswith('HEART') or str(i).endswith('LIVER'):
        target[target_index] = [0, 1, 0]  # Cow
        target_color.append(1)
    if str(i).endswith('MUSCLE') or str(i).endswith('plasma1'):
        target[target_index] = [0, 0, 1]  # Human
        target_color.append(2)
    target_index += 1


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
test_values = np.zeros(shape=(15, 3))
predicted_values = np.zeros(shape=(15, 3))

for i in range(len(df)):
    train_selection = [j for j in range(len(df)) if i != j]
    test_selection = [i]

    train_x = df[train_selection, :]
    train_y = target[train_selection]

    test_x = df[test_selection, :]
    test_y = target[test_selection]

    plsr = PLSRegression(n_components=2, scale=False)
    plsr.fit(train_x, train_y)

    predict_y = plsr.predict(test_x)

    test_values[i] = test_y
    predicted_values[i] = predict_y

    # print(np.argmax(test_y), np.argmax(predict_y))
    r2_list.append(metrics.r2_score(test_y.flatten(), predict_y.flatten()))

    ## calculate vip score
    vip_value = vip(plsr)

    index = np.argsort(vip_value)[-10:]

    # print(index, vip_value[index])

test_values = np.array(test_values)
predicted_values = np.array(predicted_values)

###############################################################
##plot for R2
# plt.scatter(test_values[:, 0], predicted_values[:, 0])
# plt.scatter(test_values[:, 1], predicted_values[:, 1])
# plt.scatter(test_values[:, 2], predicted_values[:, 2])
# plt.scatter(test_values[:, 3], predicted_values[:, 3])

r2_1 = metrics.r2_score(test_values[:, 0], predicted_values[:, 0])
r2_2 = metrics.r2_score(test_values[:, 1], predicted_values[:, 1])
r2_3 = metrics.r2_score(test_values[:, 2], predicted_values[:, 2])
# r2_4 = metrics.r2_score(test_values[:, 3], predicted_values[:, 3])
# r2_5 = metrics.r2_score(test_values[:, 4], predicted_values[:, 4])

print(r2_1, r2_2, r2_3)
####################################################

####### PLS-DA ########
plsr = PLSRegression(n_components=2, scale=False)
plsr.fit(df, target)
#######################

# calculate vip score
vip_value = vip(plsr)

# top VIP>1.5 metabolites, sort by descending way
vip_index = np.argsort(-1*vip_value)

df_out = pd.DataFrame(columns=df_origin.columns)
df_out['VIP'] = None

# n_index = 0
# for i in vip_index:
#     if vip_value[i] > 1.8:
#         df_out = df_out.append(df_origin.iloc[i])
#         df_out['VIP'].iloc[n_index] = vip_value[i]
#         n_index += 1

##### output all the compounds with their vip value
n_index = 0
for i in vip_index:
    df_out = df_out.append(df_origin.iloc[i])
    df_out['VIP'].iloc[n_index] = vip_value[i]
    n_index += 1

# ##### output top 50 vip compounds
# n_index = 0
# for i in vip_index:
#     if n_index <= 50:
#         df_out = df_out.append(df_origin.iloc[i])
#         df_out['VIP'].iloc[n_index] = vip_value[i]
#         n_index += 1


# df_out.to_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/consortium_lipid_data_new/VIP_results/'
#               'UCD_vip_greater_1.9_edit.csv')
df_out.to_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/consortium_lipid_data_new/VIP_results/'
              'Umich_all_vips.csv')

# ##### scores: The scores describe the position of each sample in each determined latent variable (LV)
scores = pd.DataFrame(plsr.x_scores_).to_numpy()

#### 2D plot for PLS-DA #######
plot = plt.scatter(scores[:, 0], scores[:, 1], c=target_color,
                   edgecolors='none', alpha=0.7, cmap=plt.cm.get_cmap('Set1', 3), s=70)
plt.xlabel("Scores on LV 1")
plt.ylabel("Scores on LV 2")
# plt.zlabel("Scores on LV 3")
classes = ["Pig", "Cow", 'Human']
plt.legend(handles=plot.legend_elements()[0], labels=classes)
# plt.clim(0, 4)
plt.title("UCD qToF Data")
##############################

plt.show()
