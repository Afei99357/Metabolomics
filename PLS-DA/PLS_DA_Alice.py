import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.cross_decomposition import PLSRegression
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

df_metabolites_info = pd.read_csv('/Users/ericliao/Downloads/ginger_data.csv', header=0, index_col=False)
df_metabolites_info = df_metabolites_info.reset_index(drop=True)

df_origin = df_metabolites_info.loc[:, "Area: coc-ctrl-13.raw (F13)":"Area: coc-12-12.raw (F12)"]

df = df_origin.fillna(0).values

## transpose df
df = df.T

## preprocessing data
scaler = StandardScaler()
df = pd.DataFrame(scaler.fit_transform(df)).values

###### create target and target color for plot######
target = np.zeros(shape=(17, 4))
target_color = []
target_index = 0
for i in df_origin.columns:
    if 'coc-ctrl' in str(i):
        target[target_index] = [1, 0, 0, 0]
        target_color.append(0)
    if 'coc-06' in str(i):
        target[target_index] = [0, 1, 0, 0]
        target_color.append(1)
    if 'coc-09' in str(i):
        target[target_index] = [0, 0, 1, 0]
        target_color.append(2)
    if 'coc-12' in str(i):
        target[target_index] = [0, 0, 0, 1]
        target_color.append(3)
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
# calculate Q2 values and store in a list
q2_list = []

# # create empty numpy array to store test values and predict values
test_values = np.zeros((17, 4))
predicted_values = np.zeros((17, 4))

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

    q2_list.append(metrics.r2_score(test_y.flatten(), predict_y.flatten()))

    ## calculate vip score
    vip_value = vip(plsr)

    index = np.argsort(vip_value)[-10:]

test_values = np.array(test_values)
predicted_values = np.array(predicted_values)

###############################################################
### Q2
q2_1 = metrics.r2_score(test_values[:, 0], predicted_values[:, 0])
q2_2 = metrics.r2_score(test_values[:, 1], predicted_values[:, 1])
q2_3 = metrics.r2_score(test_values[:, 2], predicted_values[:, 2])
q2_4 = metrics.r2_score(test_values[:, 3], predicted_values[:, 3])

print(q2_1)
print(q2_2)
print(q2_3)
print(q2_4)
####################################################

####### PLS-DA ########
plsr = PLSRegression(n_components=2, scale=False)
plsr.fit(df, target)
#######################

# calculate vip score
vip_value = vip(plsr)

vip_index = np.argsort(vip_value)

df_out = pd.DataFrame(columns=df_metabolites_info.columns)
df_out['VIP'] = None

# n_index = 0
# for i in vip_index:
#     if vip_value[i] >= 1.0:
#         df_out = df_out.append(df_metabolites_info.iloc[i])
#         df_out['VIP'].iloc[n_index] = vip_value[i]
#         n_index += 1

# df_out.to_csv('/Users/ericliao/Downloads/ginger_data_vip_greater_than_1_compounds.csv')

# ##### scores: The scores describe the position of each sample in each determined latent variable (LV)
scores = pd.DataFrame(plsr.x_scores_).to_numpy()

#### 2D plot for PLS-DA #######
plot = plt.scatter(scores[:, 0], scores[:, 1], c=target_color,
                   edgecolors='none', alpha=0.7, cmap=plt.cm.get_cmap('Set1', 4), s=70)
plt.xlabel("Scores on LV 1")
plt.ylabel("Scores on LV 2")
classes = ['coc-control: ' + str("{:.3f}".format(q2_1)), "coc-06: " + str("{:.3f}".format(q2_2)),
           "coc-09: " + str("{:.3f}".format(q2_3)), "coc-12: " + str("{:.3f}".format(q2_4))]
plt.legend(handles=plot.legend_elements()[0], labels=classes)
##############################

plt.savefig('/Users/ericliao/Downloads/ginger_data.png', dpi=300)
