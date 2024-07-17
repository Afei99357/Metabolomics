import matplotlib.pyplot as plt
import numpy
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn import model_selection
import sklearn
import os
from scipy import special

plt.style.use('ggplot')
fig = plt.figure(1, figsize=(10, 7))
plt.clf()

################### Data from consortium ################
df_origin = pd.read_csv('/Users/yliao13/Desktop/pca/LipidsWG_QEHF_POS_processed_with_mz.csv', header=0)
df = df_origin.loc[:, 'Brain1': 'Plasma13'].values
df = df.T
########################################################

########### #preprocess data using mean center#########
df = (df - df.mean(axis=1, keepdims=True)) / df.std(axis=1, keepdims=True)

# [1,0,0]-pig, [0, 1,0]-cow, [0, 0,1]-human
target = np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0],
                   [0, 1, 0, ], [0, 1, 0, ], [0, 1, 0],
                   [0, 1, 0], [0, 1, 0], [0, 1, 0],
                   [0, 0, 1], [0, 0, 1], [0, 0, 1],
                   [0, 0, 1], [0, 0, 1], [0, 0, 1]])

target_color = np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2])
######################################################

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

####### PLS-DA ########
plsr = PLSRegression(n_components=2, scale=False)
plsr.fit(df, target)

vip_values = vip(plsr)

index = np.argsort(vip_values)[-10:]
print(index, vip_values[index])

# socres: The scores describe the position of each sample in each determined latent variable (LV)
scores = pd.DataFrame(plsr.x_scores_).to_numpy()

###### 2D plot for PLS-DA #######
plot = plt.scatter(scores[:, 0], scores[:, 1], c=target_color, edgecolors='none', alpha=0.7,
                   cmap=plt.cm.get_cmap('tab20', 3), s=70)

plt.xlabel("Scores on LV 1")
plt.ylabel("Scores on LV 2")

classes = ["Pig", 'Cow', "Human"]
plt.legend(handles=plot.legend_elements()[0], labels=classes)
plt.clim(0, 3)
plt.colorbar()

#################################

# ####### 3D plot for PLS-DA #######
# ax = fig.add_subplot(111, projection='3d')
#
# ax.scatter(scores[:, 0], scores[:, 1], scores[:, 2], c=target, cmap=plt.cm.get_cmap('Set2_r', 3), s=70)
#
# ax.set_xlabel("Score on LV1")
# ax.set_ylabel("Score on LV2")
# ax.set_zlabel("Score on LV3")
# ###############################

plt.show()
