import pandas as pd
import operator
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2

### modify 1
df = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000965/aligned.csv')

df_new = df.loc[:, [' height' in i for i in df.columns]]

df_new = df_new.fillna(0)

target = []

### modify 2
# for i in df_new.columns.values:
#     if operator.contains(i, "_O"):
#         target.append(0)
#     if operator.contains(i, '_Y'):
#         target.append(1)

target = [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0],
          [0, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0],
          [0, 0, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0],
          [0, 0, 0, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]

target = np.array(target)

target_color = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3]

plsr = pls_da_model.pls_da(df_new, target, 1)

########## calculate VIPs vector ######################
vip_value = vips.vips(plsr)

vip_index = np.argsort(vip_value)

df_out = pd.DataFrame(columns=df.columns)
df_out['VIP'] = None

n_index = 0
for i in vip_index:
    if vip_value[i] >= 1.5:
        df_out = df_out.append(df.iloc[i])
        df_out['VIP'].iloc[n_index] = vip_value[i]
        n_index += 1


### modify 3
df_out.to_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/studies/ST000965/'
              '16.8mM_glucose_treatment_under_4_different_period_st000965_vip_greater_1.5_new_preprocess.csv')
#######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, target_type_number=4, axis=1)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### modify 4
target_names = ['0 min: ' + str("%.2f" % q2[0]), '30 min: ' + str("%.2f" % q2[1]),
                '60 min: ' + str("%.2f" % q2[2]), '90 min: ' + str("%.2f" % q2[3])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target_color, target_names, target_number=4)
