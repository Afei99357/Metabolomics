import pandas as pd
import operator
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
import matplotlib.pyplot as plt

### modify 1
df_train = pd.read_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/MTBLS1033/Serum/POS/with_feature_selection/train_data_80_percent.csv"
)

df_factor = pd.read_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/"
    "data_files/MTBLS1033/Serum/POS/with_feature_selection/test_data_20_percent.csv"
)

df_test = pd.read_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/MTBLS1033/Serum/POS/"
    "with_feature_selection/test_data_20_percent.csv",
    index_col=0,
    header=0,
)

df_height_train = df_train.loc[:, [" height" in i for i in df_train.columns]]


df_height_train = df_height_train.fillna(0)

train_data_list = []

train_samples_names = df_height_train.columns.values.tolist()
test_samples_names = df_test.index.values.tolist()

for i in train_samples_names:
    if i not in test_samples_names:
        train_data_list.append(i)

df_height_train = df_height_train[train_data_list]

df_height_transposed_train = df_height_train.T

# train_df = df_height_transposed_train[[]]

data_list = []
target_train = []

for index, row in df_height_transposed_train.iterrows():
    source_name = index.split(" ", 1)[0].strip()

    treatment_type = df_factor[df_factor["Source Name"] == source_name][
        "Factor Value[Group]"
    ].values[0]

    if operator.contains(treatment_type, "Control"):
        row_dict = row.to_dict()
        data_list.append(row_dict)
        target_train.append(0)

    if operator.contains(treatment_type, "POP"):
        row_dict = row.to_dict()
        data_list.append(row_dict)
        target_train.append(1)

target_train = np.array(target_train)

df_new_train = pd.DataFrame.from_dict(data_list)

scaler = StandardScaler()

df_new_train = pd.DataFrame(scaler.fit_transform(df_new_train)).values

####### PLS-DA ########
plsr = PLSRegression(n_components=2, scale=False)
plsr.fit(df_new_train, target_train)
#
# test_x = df_test.iloc[:, :-1]
# test_x = pd.DataFrame(scaler.fit_transform(test_x)).values
#
# test_y = np.array(df_test.iloc[:, -1].tolist())
#
#
# predict_y = plsr.predict(test_x)
#
# q2 = metrics.r2_score(test_y.flatten(), predict_y.flatten())
q2 = calculate_q2.calculate_q2_k_fold(
    df_test, np.array(df_test.iloc[:, -1].tolist()), 0, 4
)
print(q2)

target_names = [
    "Control Group: " + str("%.2f" % q2[0]),
    "POP Group: " + str("%.2f" % q2[0]),
]
target_names = np.array(target_names)

scores = pd.DataFrame(plsr.x_scores_).to_numpy()
plot_2d.plsda_2d_plot(scores, target_train, target_names, 2)


# ### CIs (confidence intervals)
# def roc_auc_ci(y_true, y_score, positive=1):
#     AUC = metrics.roc_auc_score(y_true, y_score)
#     N1 = sum(y_true == positive)
#     N2 = sum(y_true != positive)
#     Q1 = AUC / (2 - AUC)
#     Q2 = 2*AUC**2 / (1 + AUC)
#     SE_AUC = sqrt((AUC*(1 - AUC) + (N1 - 1)*(Q1 - AUC**2) + (N2 - 1)*(Q2 - AUC**2)) / (N1*N2))
#     print(SE_AUC)
#
#     ## Zcrit = 1.96 when a = 0.05 (95% confidence intervals)
#     lower = AUC - 1.96*SE_AUC
#     upper = AUC + 1.96*SE_AUC
#     if lower < 0:
#         lower = 0
#     if upper > 1:
#         upper = 1
#     return lower, upper
#
# ci = roc_auc_ci(test_y, predict_y)
#
# print(ci)
#

for i in range(len(q2[1])):
    fpr, tpr = q2[2][i][0], q2[2][i][1]
    auc = q2[1][i]
    plt.plot(fpr, tpr, label="AUC=" + str(auc))
    plt.text(
        5.5,
        0.5,
        "TEST TEST TEST TEST",
        bbox={"facecolor": "white", "alpha": 1, "edgecolor": "none", "pad": 1},
        ha="center",
        va="center",
    )
    plt.ylabel("True Positive Rate")
    plt.xlabel("False Positive Rate")
    plt.legend(loc=4)
plt.show()
