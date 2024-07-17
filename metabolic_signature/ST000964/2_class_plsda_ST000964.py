import pandas as pd
import operator
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2

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

df_out.to_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000964/results/old_vs_young_st000964_vip_greater_0.csv')
#######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_height, target, 2, 1)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

target_names = ['Old: ' + str("%.2f" % q2[0]), 'Young: ' + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'Old vs Young')

##### End of Block 1: plsda for old vs young################



# ##### Begin of Block 2: plsda for 16.8 mM vs 2.8 mM ################
target = []
for i in df_height.columns.values:
    treatment = df_factor[df_factor['local_sample_id'] == i.split('.', 1)[0]]['Treatment'].values[0]
    if operator.contains(treatment, "2.8mM"):
        target.append(0)
    if operator.contains(treatment, '16.8mM'):
        target.append(1)
target = np.array(target)

plsr = pls_da_model.pls_da(df_height, target, 1)

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

df_out.to_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000964/results/2.8mM_vs_16.8mM_st000964_vip_greater_0.csv')
#######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_height, target, 2, 1)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

target_names = ['2.8mM: ' + str("%.2f" % q2[0]), '16.8mM: ' + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, '16.8 mM vs 2.8 mM')

##### End of Block 2: plsda for 16.8 mM vs 2.8 mM ################



##### Begin of Block 3: plsda for old 16.8 mM vs young 16.8 mM ################
df_transpose = df_height.T
df_new = pd.DataFrame(columns=df.T.columns)
target = []

for index, row in df_transpose.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    treatment = df_factor[df_factor['local_sample_id'] == local_sample_id]['Treatment'].values[0]
    age = df_factor[df_factor['local_sample_id'] == local_sample_id]['Age'].values[0]

    if operator.contains(age, "Old") and operator.contains(treatment, "16.8mM"):
        df_new = df_new.append(row)
        target.append(0)
    if operator.contains(age, "Young") and operator.contains(treatment, "16.8mM"):
        df_new = df_new.append(row)
        target.append(1)

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

df_out.to_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000964/results/old_16.8mM_vs_young_16.8mM_st000964_vip_greater_0.csv')
#######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

target_names = ['Old 16.8mM: ' + str("%.2f" % q2[0]), 'Young 16.8mM: ' + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'old 16.8 mM vs young 16.8 mM')

##### End of Block 3: plsda for old 16.8 mM vs young 16.8 mM ################



##### Begin of Block 4: plsda for old 2.8 mM vs young 2.8 mM ################
df_transpose = df_height.T
df_new = pd.DataFrame(columns=df.T.columns)
target = []

for index, row in df_transpose.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    treatment = df_factor[df_factor['local_sample_id'] == local_sample_id]['Treatment'].values[0]
    age = df_factor[df_factor['local_sample_id'] == local_sample_id]['Age'].values[0]

    if operator.contains(age, "Old") and operator.contains(treatment, "2.8mM"):
        df_new = df_new.append(row)
        target.append(0)
    if operator.contains(age, "Young") and operator.contains(treatment, "2.8mM"):
        df_new = df_new.append(row)
        target.append(1)

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

df_out.to_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000964/results/old_2.8mM_vs_young_2.8mM_st000964_vip_greater_0.csv')
#######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

target_names = ['Old 2.8mM: ' + str("%.2f" % q2[0]), 'Young 2.8mM: ' + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'old 2.8 mM vs young 2.8 mM')

##### End of Block 4: plsda for old 2.8 mM vs young 2.8 mM ################
