import pandas as pd
import operator
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2
import matplotlib.pyplot as plt

### load data
df = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000603/data/aligned.csv')
df_factor = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000603/data/factors.csv')

for index, item in df_factor.iterrows():
    item['local_sample_id'] = item['local_sample_id'].strip()

df_height = df.loc[:, [' height' in i for i in df.columns]]
df_height = df_height.fillna(0)
df_height_transposed = df_height.T

##### Begin of Block 1: plsda for control group and IC group (Interstitial cystitis) ################

df_new = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    treatment = df_factor[df_factor['local_sample_id'] == local_sample_id]['Treatment'].values[0]

    if operator.contains(treatment, "control"):
        target.append(0)
        df_new = df_new.append(row)
    if operator.contains(treatment, "IC"):
        target.append(1)
        df_new = df_new.append(row)

target = np.array(target)

plsr = pls_da_model.pls_da(df_new, target, 0)

########## calculate VIPs vector ######################
vip_value = vips.vips(plsr)

vip_index = np.argsort(vip_value)

df_out = pd.DataFrame(columns=df.columns)
df_out['VIP'] = None

n_index = 0
for i in vip_index:
    if vip_value[i] >= 0:
        df_out = df_out.append(df.iloc[i])
        df_out['VIP'].iloc[n_index] = vip_value[i]
        n_index += 1


## output metabolites vip score
# df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000603/results/control_vs_IC_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['Control Q2: ' + str("%.2f" % q2[0]), 'IC Q2' + ": " + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, sample_labels_list=df_new.index.tolist())



##### End of Block 1: plsda for Deprive of Glucose and Deprive of Glutamine ################