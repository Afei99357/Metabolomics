import pandas as pd
import operator
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2


df = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000396/data/aligned.csv')
df_factor = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000396/data/factors.csv')

df_height = df.loc[:, [' height' in i for i in df.columns]]
df_height = df_height.fillna(0)
df_height_transposed = df_height.T


##### Begin of Block 1: plsda for current and former smoker ################
df_new = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    status = df_factor[df_factor['local_sample_id'] == local_sample_id]['Smoking Status'].values[0]

    if operator.contains(status, "Former"):
        target.append(0)
        df_new = df_new.append(row)
    if operator.contains(status, "Current"):
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


### modify 3
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000396/results/former_vs_current.csv')
#######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### modify 4
target_names = ['former: ' + str("%.2f" % q2[0]), 'current' + ': ' + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'former smoker vs. current smoker')

##### End of Block 1: plsda for current and former smoker ################



##### Begin of Block 2: plsda for current and former smoker in different age group ################
age = ['50-54', '55-59', '60-64']

for item in age:
    df_age = pd.DataFrame(columns=df_height_transposed.columns)
    target = []
    for index, row in df_height_transposed.iterrows():
        local_sample_id = index.split(".", 1)[0].strip()
        status = df_factor[df_factor['local_sample_id'] == local_sample_id]['Smoking Status'].values[0]
        age = df_factor[df_factor['local_sample_id'] == local_sample_id]['Age Group'].values[0]
        if operator.contains(age, item) and operator.contains(status, "Former"):
            target.append(0)
            df_age = df_age.append(row)
        if operator.contains(age, item) and operator.contains(status, "Current"):
            target.append(1)
            df_age = df_age.append(row)

    target = np.array(target)

    plsr = pls_da_model.pls_da(df_age, target, 0)

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


    ### modify 3
    df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000396/results/former_vs_current_in' + item + '_group.csv')
    #######################################################

    ######### print out the q2 with leave one out cross-validation #####
    q2 = calculate_q2.calculate_q2(df_age, target, 2, 0)
    ####################################################################

    ######### scores: The scores describe the position of
    ### each sample in each determined latent variable (LV)####
    scores = pd.DataFrame(plsr.x_scores_).to_numpy()
    ###############################################################

    ### modify 4
    target_names = ['former: ' + str("%.2f" % q2[0]), 'current' + ': ' + str("%.2f" % q2[1])]
    target_names = np.array(target_names)

    plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'former smoker vs. current smoker in group '+item)

##### End of Block 2: plsda for current and former smoker in different age group ################



##### Begin of Block 3: plsda for diseas and non-disease smoker ################
df_disease = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    diagnosis = df_factor[df_factor['local_sample_id'] == local_sample_id]['Diagnosis'].values[0]

    if operator.contains(diagnosis, "-"):
        target.append(0)
        df_disease = df_disease.append(row)
    else:
        target.append(1)
        df_disease = df_disease.append(row)

target = np.array(target)

plsr = pls_da_model.pls_da(df_disease, target, 0)

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


### modify 3
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000396/results/non-disease_vs_disease.csv')
#######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_disease, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### modify 4
target_names = ['non_disease: ' + str("%.2f" % q2[0]), 'disease' + ': ' + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'non-disease vs. diseaase')
##### End of Block 3: plsda for diseas and non-disease smoker ################


##### Start of Block 4: plsda for diseas and non-disease smoker in different smoking status ################
status = ['Current', 'Former']

for item in status:
    df_new = pd.DataFrame(columns=df_height_transposed.columns)
    target = []
    for index, row in df_height_transposed.iterrows():
        local_sample_id = index.split(".", 1)[0].strip()
        status = df_factor[df_factor['local_sample_id'] == local_sample_id]['Smoking Status'].values[0]
        disease = df_factor[df_factor['local_sample_id'] == local_sample_id]['Diagnosis'].values[0]
        if operator.contains(status, item) and operator.contains(disease, "-"):
            target.append(0)
            df_new = df_new.append(row)
        if operator.contains(status, item) and not operator.contains(disease, "-"):
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


    ### modify 3
    df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000396/results/former_vs_current_in' + item + '_group.csv')
    #######################################################

    ######### print out the q2 with leave one out cross-validation #####
    q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
    ####################################################################

    ######### scores: The scores describe the position of
    ### each sample in each determined latent variable (LV)####
    scores = pd.DataFrame(plsr.x_scores_).to_numpy()
    ###############################################################

    ### modify 4
    target_names = ['former: ' + str("%.2f" % q2[0]), 'current' + ': ' + str("%.2f" % q2[1])]
    target_names = np.array(target_names)

    plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'former smoker vs. current smoker in group '+item)

##### End of Block 4: plsda for diseas and non-disease smoker in different smoking status ################