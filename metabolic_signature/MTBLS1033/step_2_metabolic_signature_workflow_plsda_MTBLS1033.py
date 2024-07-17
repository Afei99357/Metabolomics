import pandas as pd
import operator
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.vips import vips
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
import matplotlib.pyplot as plt

### read in data
df = pd.read_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/NEG/aligned.csv"
)
df_factor = pd.read_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/NEG/MTBLS1033_factors.csv"
)

df_height = df.loc[:, [" height" in i for i in df.columns]]
df_height = df_height.fillna(0)
df_height_transposed = df_height.T


#### obtain the data we need and target information
data_list = []
target = []
index_list = []

for index, row in df_height_transposed.iterrows():
    source_name = index.split(" ", 1)[0].strip()

    treatment_type = df_factor[df_factor["Source Name"] == source_name][
        "Factor Value[Group]"
    ].values[0]

    if operator.contains(treatment_type, "Control"):
        target.append(0)
        row_dict = row.to_dict()
        data_list.append(row_dict)
        index_list.append(source_name)

    if operator.contains(treatment_type, "POP"):
        target.append(1)
        row_dict = row.to_dict()
        data_list.append(row_dict)
        index_list.append(source_name)

target = np.array(target)

df_new = pd.DataFrame.from_dict(data_list)

df_new.index = index_list

df_new["target"] = target


#### separate training and testing data
training_data, testing_data = train_test_split(
    df_new, test_size=0.2, random_state=25
)

# testing_data.to_csv(
#     "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/MTBLS1033/Urine/POS/new_analysis/with_feature_selection/test_data_20_percent.csv"
# )
# training_data.to_csv(
#     "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/MTBLS1033/Urine/POS/new_analysis/with_feature_selection/train_data_80_percent.csv"
# )


#### train the PLS-DA model with training data
plsr = pls_da_model.pls_da(
    training_data.iloc[:, :-1],
    np.array(training_data.iloc[:, -1].tolist()),
    0,
)

######### calculate VIPs vector and attach vip to each metabolite
vip_value = vips.vips(plsr)

vip_index = np.argsort(vip_value)

df_out_with_vips = pd.DataFrame(columns=df.columns)
df_out_with_vips["VIP"] = None
vip_data_list = []

n_index = 0
for i in vip_index:
    if vip_value[i] >= 0:
        row_dict = df.iloc[i].to_dict()
        row_dict["VIP"] = vip_value[i]
        vip_data_list.append(row_dict)
        n_index += 1

df_out_with_vips = pd.DataFrame.from_dict(vip_data_list)

# output metabolites vip score
# df_out_with_vips.to_csv(
#     "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/MTBLS1033/Urine/POS/new_analysis/with_feature_selection/vips.csv"
# )

######################################################
######################################################

#### load file from the NIST library matching result
df_match = pd.read_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/NEG/matched.csv",
    header=0,
    index_col=None,
)

#### get sample names from df_match df
values_list = pd.Series(
    list({item["Unknown"].split(" [", 2)[0] for index, item in df_match.iterrows()}),
    name="name",
)

#### filter out metabolites have match from NIST library and keep the VIPS
df_out_annotated_with_vip = df_out_with_vips.merge(values_list, on="name", how="inner")

# df_out_annotated_with_vip.to_csv(
#     "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/MTBLS1033/Urine/POS/new_analysis/with_feature_selection/vips_annotated.csv"
# )

#### only keep the top 10 vip metabolights which are annotated / matched
df_top10_vip_matches = df_out_annotated_with_vip.sort_values(
    by=["VIP"], ascending=False
).iloc[0:10, :]

# df_top10_vip_matches.to_csv(
#     "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/MTBLS1033/Urine/POS/new_analysis/with_feature_selection/vips_top10_annotated.csv"
# )


######################################################
#
# to train and test pls-da using the chosen top 10 vip metabolites data
#
######################################################

### grab the top10 metabolites index to obtain the dataframe from the original train and test dataset
top10_metabolites_index_list = df_top10_vip_matches["position"].tolist()
column_name_list = []

for i in top10_metabolites_index_list:
    column_name_list.append(i - 1)

training_data_top10 = training_data[[i for i in column_name_list]]
testing_data_top10 = testing_data[[i for i in column_name_list]]
# df = df.fillna(0)

target_train_top10 = []
target_test_top10 = []

for i in training_data_top10.index:
    treatment_type = df_factor[df_factor["Source Name"] == i][
        "Factor Value[Group]"
    ].values[0]
    if operator.contains(treatment_type, "Control"):
        target_train_top10.append(0)

    if operator.contains(treatment_type, "POP"):
        target_train_top10.append(1)

for i in testing_data_top10.index:
    treatment_type = df_factor[df_factor["Source Name"] == i][
        "Factor Value[Group]"
    ].values[0]
    if operator.contains(treatment_type, "Control"):
        target_test_top10.append(0)

    if operator.contains(treatment_type, "POP"):
        target_test_top10.append(1)

target_train_top10 = np.array(target_train_top10)
target_test_top10 = np.array(target_test_top10)

scaler = StandardScaler()

df_train_top10_new = pd.DataFrame(scaler.fit_transform(training_data_top10)).values

####### PLS-DA ########
plsr_top10 = PLSRegression(n_components=2, scale=False)
plsr_top10.fit(df_train_top10_new, target_train_top10)
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
q2 = calculate_q2.calculate_q2_k_fold(testing_data_top10, target_test_top10, 0, 4)

### get 95% confidence intervals
cis = q2[3]

print(q2)

target_names = [
    "Control Group: " + str("%.2f" % q2[0]),
    "POP Group: " + str("%.2f" % q2[0]),
]
target_names = np.array(target_names)

scores = pd.DataFrame(plsr_top10.x_scores_).to_numpy()
plot_2d.plsda_2d_plot(scores, target_train_top10, target_names, 2)


## plot ROC_AUC curve
for i in range(len(q2[1])):
    fpr, tpr = q2[2][i][0], q2[2][i][1]
    auc = q2[1][i]
    plt.plot(fpr, tpr, label="AUC=" + str(auc))
    plt.text(
        0.5,
        0.5,
        "95% Confidence Intervals: " + str(q2[3]),
        bbox={"facecolor": "white", "alpha": 1, "edgecolor": "none", "pad": 1},
        ha="center",
        va="center",
    )
    plt.ylabel("True Positive Rate")
    plt.xlabel("False Positive Rate")
    plt.legend(loc=4)

plt.show()
