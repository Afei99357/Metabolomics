import pandas as pd
import numpy as np
import operator
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2

### load data
# df = pd.read_csv('./data/aligned.csv')
# df_factor = pd.read_csv('./data/factors.csv')

df = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000548/data/aligned.csv')
df_factor = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000548/data/factors.csv')

df_height = df.loc[:, [' height' in i for i in df.columns]]

df_height = df_height.fillna(0)

##### Begin of Block 1: plsda for WT vs. MUT vs. V in 24 hours ################
target = []
target_color = []
for i in df_height.columns.values:
    if operator.contains(i, "_24"):
        if operator.contains(i, "_WT"):
            target.append([1, 0, 0])
            target_color.append(0)
        if operator.contains(i, '_MUT'):
            target.append([0, 1, 0])
            target_color.append(1)
        if operator.contains(i, '_V'):
            target.append([0, 0, 1])
            target_color.append(2)

target = np.array(target)

df_24hour = df_height.loc[:, ['_24' in i for i in df_height.columns]]

plsr = pls_da_model.pls_da(df_24hour, target, 1)

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

df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000548/results/24hour_WT_vs_MUT_vs_V_vip_greater_0.csv')
#######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_24hour, target, 3, 1)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

target_names = ['WT: ' + str("%.2f" % q2[0]), 'MUT: ' + str("%.2f" % q2[1]), 'V: ' + str("%.2f" % q2[2])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target_color, target_names, 3, 'WT vs. MUT vs. V plsda plot')

##### End of Block 1: plsda for WT vs. MUT vs. V in 24 hours ################


# ##### Begin of Block 2: plsda for WT vs. MUT vs. V in 48 hours ################
df_transpose = df_height.T
df_48hour = pd.DataFrame(columns=df.T.columns)
target = []
target_color = []

for index, row in df_transpose.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    time = df_factor[df_factor['local_sample_id'] == local_sample_id]['Time Point'].values[0]

    if operator.contains(time, "48"):
        df_48hour = df_48hour.append(row)

for index, row in df_48hour.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    if operator.contains(local_sample_id, "_WT"):
        target.append([1, 0, 0])
        target_color.append(0)
    if operator.contains(local_sample_id, '_MUT'):
        target.append([0, 1, 0])
        target_color.append(1)
    if operator.contains(local_sample_id, '_V'):
        target.append([0, 0, 1])
        target_color.append(2)


target = np.array(target)

plsr = pls_da_model.pls_da(df_48hour, target, 0)

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

df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000548/results/48hour_WT_vs_MUT_vs_V_vip_greater_0.csv')
#######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_48hour, target, 3, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

target_names = ['WT: ' + str("%.2f" % q2[0]), 'MUT: ' + str("%.2f" % q2[1]), 'V: ' + str("%.2f" % q2[2])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target_color, target_names, 3, 'WT vs. MUT vs. V plsda plot')

##### End of Block 2: plsda for WT vs. MUT vs. V in 48 hours ################


##### Begin of Block 3: plsda for WT vs. MUT vs. V in HR hours ################
target = []
target_color = []
for i in df_height.columns.values:
    if operator.contains(i, "_HR"):
        if operator.contains(i, "_WT"):
            target.append([1, 0, 0])
            target_color.append(0)
        if operator.contains(i, '_IDH2'):
            target.append([0, 1, 0])
            target_color.append(1)
        if operator.contains(i, '_IDH1'):
            target.append([0, 0, 1])
            target_color.append(2)

target = np.array(target)

df_HR = df_height.loc[:, ['_HR' in i for i in df_height.columns]]

plsr = pls_da_model.pls_da(df_HR, target, 1)

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

df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000548/results/HR_hour_WT_vs_IDH2_vs_IDH1_vip_greater_0.csv')
#######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_HR, target, 3, 1)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

target_names = ['WT: ' + str("%.2f" % q2[0]), 'IDH2: ' + str("%.2f" % q2[1]), 'IDH1: ' + str("%.2f" % q2[2])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target_color, target_names, 3, 'WT vs. IDH2 vs. IDH1 plsda plot')

##### End of Block 3: plsda for WT vs. MUT vs. V in HR hours ################
