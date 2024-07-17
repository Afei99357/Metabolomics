import operator

import numpy as np
import pandas as pd

from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips

### modify 1
df = pd.read_csv("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS4497/aligned.csv")
df_factor = pd.read_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS4497/MTBLS4497_factors_remove.csv"
)

df_height = df.loc[:, [' height' in i for i in df.columns]]
df_height = df_height.fillna(0)
df_height_transposed = df_height.T

#### obtain the data we need and target information
data_list = []
target = []
index_list = []

for index, row in df_height_transposed.iterrows():
    source_name = index.split(" ", 1)[0].strip()
    treatment = df_factor[df_factor["Sample Name"] == source_name][
        "Factor Value[Treatment]"
    ].values[0]

    if operator.contains(treatment, "alpha-ketoisovalerate"):
        target.append(0)
        row_dict = row.to_dict()
        data_list.append(row_dict)
        index_list.append(source_name)

    if not operator.contains(treatment, "alpha-ketoisovalerate"):
        target.append(1)
        row_dict = row.to_dict()
        data_list.append(row_dict)
        index_list.append(source_name)

target = np.array(target)

df_new = pd.DataFrame.from_dict(data_list)

df_new.index = index_list

df_new["target"] = target

plsr = pls_da_model.pls_da(df_new, target, 0)

########## calculate VIPs vector ######################
# vip_value = vips.vips(plsr)
#
# vip_index = np.argsort(vip_value)
#
# df_out = pd.DataFrame(columns=df.columns)
# df_out["VIP"] = None
# vip_data_list = []
#
# n_index = 0
# for i in vip_index:
#     if vip_value[i] >= 0:
#         row_dict = df.iloc[i].to_dict()
#         row_dict["VIP"] = vip_value[i]
#         vip_data_list.append(row_dict)
#         n_index += 1
#
# df_out = pd.DataFrame.from_dict(vip_data_list)

# ## output metabolites vip score
# df_out.to_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000058/0_hour_vs_' + time + '_st000058_vip_greater_0.csv')
# ######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
# q2 = calculate_q2.calculate_q2_k_fold(df_new, target, 0, 4)

####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### modify 4
target_names = [
    "KIV: " + str("%.2f" % q2[0]),
    "Non-KIV: " + str("%.2f" % q2[0]),
]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2)
