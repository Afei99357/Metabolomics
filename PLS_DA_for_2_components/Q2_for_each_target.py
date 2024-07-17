# Author: Eric Liao
# August 2021

from sklearn import metrics
import numpy as np
from sklearn.cross_decomposition import PLSRegression
import pandas as pd
from sklearn.preprocessing import StandardScaler
from math import sqrt

from sklearn.model_selection import StratifiedKFold


class calculate_q2:
    def calculate_q2_k_fold(df, target, axis, k_fold):
        ####### leave one out cross validation #######################
        # calculate R2 values and store in a list
        q2_list = []
        auc_list = []
        fpr_tpr_list = []

        kf = StratifiedKFold(n_splits=k_fold)
        X = df.iloc[:, :-1]

        # kf.get_n_splits(X)

        scaler = StandardScaler()
        # # create empty numpy array to store test values and predict values
        target_type_number = 2
        test_values = []
        predicted_values = []

        index = 0
        for train_index, test_index in kf.split(X, target):
            train_x, test_x = X.iloc[train_index, :], X.iloc[test_index, :]
            train_y, test_y = target[train_index], target[test_index]

            if axis == 0:
                #### pre-processing data###
                train_x = pd.DataFrame(scaler.fit_transform(train_x)).values
                test_x = pd.DataFrame(scaler.fit_transform(test_x)).values
            else:
                ## remove the first row which is target names
                train_x = train_x.iloc[1:, :]
                train_x = train_x.T
                #### pre-processing data###
                train_x = pd.DataFrame(scaler.fit_transform(train_x)).values

                test_x = train_x.iloc[1:, :]
                test_x = test_x.T
                #### pre-processing data###
                test_x = pd.DataFrame(scaler.fit_transform(test_x)).values

            plsr = PLSRegression(n_components=2, scale=False)
            plsr.fit(train_x, train_y)

            predict_y = plsr.predict(test_x)
            test_values.extend(test_y)
            predicted_values.extend(predict_y[:, 0].tolist())

            ### ROC and AUC
            fpr, tpr, _ = metrics.roc_curve(test_y, predict_y)
            auc = metrics.roc_auc_score(test_y, predict_y)

            ######### calculate CIs start ###########
            positive = 1
            N1 = sum(test_y == positive)
            N2 = sum(test_y != positive)
            Q1 = auc / (2 - auc)
            Q2 = 2 * auc**2 / (1 + auc)
            SE_AUC = sqrt(
                (
                    auc * (1 - auc)
                    + (N1 - 1) * (Q1 - auc**2)
                    + (N2 - 1) * (Q2 - auc**2)
                )
                / (N1 * N2)
            )

            ## Zcrit = 1.96 when a = 0.05 (95% confidence intervals)
            lower = auc - 1.96 * SE_AUC
            upper = auc + 1.96 * SE_AUC
            if lower < 0:
                lower = 0
            if upper > 1:
                upper = 1
            ci_range = [lower, upper]
            ######### calculate CIs end###########

            auc_list.append(auc)
            fpr_tpr_list.append([fpr, tpr])

            # q2_list.append(metrics.r2_score(test_y.flatten(), predict_y.flatten()))
            index = index + 1

        q2_1 = metrics.r2_score(test_values, predicted_values)

        # q2_2 = metrics.r2_score(test_values[:, 1], predicted_values[:, 1])
        return [q2_1, auc_list, fpr_tpr_list, ci_range]

    def calculate_q2(df, target, target_type_number, axis):
        ####### leave one out cross validation #######################
        # calculate R2 values and store in a list
        q2_list = []

        ## create empty numpy array to store test values and predict values
        test_values = np.zeros(shape=(len(target), target_type_number))
        predicted_values = np.zeros(shape=(len(target), target_type_number))

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
            q2_list.append(metrics.r2_score(test_y.flatten(), predict_y.flatten()))

        test_values = np.array(test_values)
        predicted_values = np.array(predicted_values)

        if target_type_number == 2:
            q2_1 = metrics.r2_score(test_values[:], predicted_values[:])
            q2_2 = metrics.r2_score(test_values[:, 1], predicted_values[:, 1])
            return [q2_1, q2_2]

            print("Q2 are:" + str(q2_1) + " and " + str(q2_2))

        if target_type_number == 3:
            q2_1 = metrics.r2_score(test_values[:], predicted_values[:])
            q2_2 = metrics.r2_score(test_values[:, 1], predicted_values[:, 1])
            q2_3 = metrics.r2_score(test_values[:, 2], predicted_values[:, 2])
            return [q2_1, q2_2, q2_3]
            print("Q2 are:" + str(q2_1) + ", " + str(q2_2) + ", " + str(q2_3))

        if target_type_number == 4:
            q2_1 = metrics.r2_score(test_values[:], predicted_values[:])
            q2_2 = metrics.r2_score(test_values[:, 1], predicted_values[:, 1])
            q2_3 = metrics.r2_score(test_values[:, 2], predicted_values[:, 2])
            q2_4 = metrics.r2_score(test_values[:, 3], predicted_values[:, 3])
            return [q2_1, q2_2, q2_3, q2_4]
            print(
                "Q2 are:"
                + str(q2_1)
                + ", "
                + str(q2_2)
                + ", "
                + str(q2_3)
                + ", "
                + str(q2_4)
            )

        if target_type_number == 5:
            q2_1 = metrics.r2_score(test_values[:], predicted_values[:])
            q2_2 = metrics.r2_score(test_values[:, 1], predicted_values[:, 1])
            q2_3 = metrics.r2_score(test_values[:, 2], predicted_values[:, 2])
            q2_4 = metrics.r2_score(test_values[:, 3], predicted_values[:, 3])
            q2_5 = metrics.r2_score(test_values[:, 4], predicted_values[:, 4])
            return [q2_1, q2_2, q2_3, q2_4, q2_5]
            print(
                "Q2 are:"
                + str(q2_1)
                + ", "
                + str(q2_2)
                + ", "
                + str(q2_3)
                + ", "
                + str(q2_4)
                + ", "
                + str(q2_5)
            )

        if target_type_number == 6:
            q2_1 = metrics.r2_score(test_values[:], predicted_values[:])
            q2_2 = metrics.r2_score(test_values[:, 1], predicted_values[:, 1])
            q2_3 = metrics.r2_score(test_values[:, 2], predicted_values[:, 2])
            q2_4 = metrics.r2_score(test_values[:, 3], predicted_values[:, 3])
            q2_5 = metrics.r2_score(test_values[:, 4], predicted_values[:, 4])
            q2_6 = metrics.r2_score(test_values[:, 5], predicted_values[:, 5])
            return [q2_1, q2_2, q2_3, q2_4, q2_5, q2_6]
            print(
                "Q2 are:"
                + str(q2_1)
                + ", "
                + str(q2_2)
                + ", "
                + str(q2_3)
                + ", "
                + str(q2_4)
                + ", "
                + str(q2_5)
                + ", "
                + str(q2_6)
            )
