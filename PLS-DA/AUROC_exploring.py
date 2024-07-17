import pandas as pd
import operator
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from sklearn import metrics
from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt

### upload data
df = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000964/data/aligned.csv')
df_factor = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000964/data/factors.csv')

df_height = df.loc[:, [' height' in i for i in df.columns]]

df_height = df_height.fillna(0)

##### Begin of Block 1: plsda for old vs young################
target = []
for i in df_height.columns.values:
    if operator.contains(i, "_O"):
        target.append(0)
    if operator.contains(i, '_Y'):
        target.append(1)

target = np.array(target)

plsr = pls_da_model.pls_da(df_height, target, 1)

def calculate_auroc(df, target, axis, threshold):



    # # create empty numpy array to store test values and predict values
    test_values = np.zeros(shape=(len(target), 2))
    predicted_values = np.zeros(shape=(len(target), 2))

    scaler = StandardScaler()
    if axis == 0:
        #### pre-processing data###
        df = pd.DataFrame(scaler.fit_transform(df)).values
    else:
        ## remove the first row which is target names
        df = df.iloc[1:, :]
        df = df.T
        #### pre-processing data###
        df = pd.DataFrame(scaler.fit_transform(df)).values

    ####### leave one out cross validation #######################
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

        auroc_list = []
        for threshold in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
            new_predict_y = []
            for m in predict_y:
                if m < threshold:
                    new_predict_y.append(0)
                if m >= threshold:
                    new_predict_y.append(1)

            auroc_list.append(roc_auc_score(test_y, new_predict_y))

        plot = plt.scatter()



# calculate auroc values and store in a list

auroc_score = calculate_auroc(df_height, target, 2, 0.5)
