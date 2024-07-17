import pandas as pd
import operator
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2

### load data
df = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000910/data/aligned.csv')
df_factor = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000910/data/factors.csv')

for index, item in df_factor.iterrows():
    item['local_sample_id'] = item['local_sample_id'].strip()

df_height = df.loc[:, [' height' in i for i in df.columns]]
df_height = df_height.fillna(0)
df_height_transposed = df_height.T

## ND -- no neurological disease (no disease),
## MECFS -- ME/CFS (disease patient),
## MS -- multiple sclerosis (disease patients)
## Mannose was a cardinal biomarker in ME/CFS subjects with reduced levels in ME/CFS compared to both MS and ND subjects.
## Levels of acetylcarnitine were reduced in ME/CFS vs. MS subjects.


##### Begin of Block 1: plsda for ND verse MECFS ################
df_new = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    diagnosis = df_factor[df_factor['local_sample_id'] == local_sample_id]['Diagnosis'].values[0]

    if operator.contains(diagnosis, "ND"):
        target.append(0)
        df_new = df_new.append(row)
    if operator.contains(diagnosis, "MECFS"):
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
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000910/results/ND_vs_MECFS_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['ND: ' + str("%.2f" % q2[0]), 'ME/CFS' + ": " + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'PLS-DA for ND verse MECFS')
##### End of Block 1: plsda for ND verse ME/CFS ################


##### Begin of Block 2: plsda for ND verse MS ################
df_new = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    diagnosis = df_factor[df_factor['local_sample_id'] == local_sample_id]['Diagnosis'].values[0]

    if operator.contains(diagnosis, "ND"):
        target.append(0)
        df_new = df_new.append(row)
    if operator.contains(diagnosis, "MS"):
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
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000910/results/ND_vs_MS_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['ND: ' + str("%.2f" % q2[0]), 'MS' + ": " + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'PLS-DA for ND verse MS')
##### End of Block 2: plsda for ND verse MS ################


##### Begin of Block 3: plsda for ND verse ME/CFS Male ################
df_new = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    diagnosis = df_factor[df_factor['local_sample_id'] == local_sample_id]['Diagnosis'].values[0]
    sex = df_factor[df_factor['local_sample_id'] == local_sample_id]['Sex'].values[0]

    if operator.contains(diagnosis, "ND") and sex == 'MALE':
        target.append(0)
        df_new = df_new.append(row)
    if operator.contains(diagnosis, "MECFS") and sex == 'MALE':
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
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000910/results/ND_male_vs_MECFS_male_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['ND male: ' + str("%.2f" % q2[0]), 'ME/CFS male' + ": " + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'PLS-DA for ND_male verse MECFS male')
##### End of Block 3: plsda for ND verse ME/CFS Male ################

##### Begin of Block 4: plsda for ND verse ME/CFS Female ################
df_new = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    diagnosis = df_factor[df_factor['local_sample_id'] == local_sample_id]['Diagnosis'].values[0]
    sex = df_factor[df_factor['local_sample_id'] == local_sample_id]['Sex'].values[0]

    if operator.contains(diagnosis, "ND") and sex == 'FEMALE':
        target.append(0)
        df_new = df_new.append(row)
    if operator.contains(diagnosis, "MECFS") and sex == 'FEMALE':
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
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000910/results/ND_female_vs_MECFS_female_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['ND female: ' + str("%.2f" % q2[0]), 'ME/CFS female' + ": " + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'PLS-DA for ND female verse MECFS female')
##### End of Block 4: plsda for ND verse ME/CFS Female ################


##### Begin of Block 5: plsda for ND male verse MS male ################
df_new = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    diagnosis = df_factor[df_factor['local_sample_id'] == local_sample_id]['Diagnosis'].values[0]
    sex = df_factor[df_factor['local_sample_id'] == local_sample_id]['Sex'].values[0]

    if operator.contains(diagnosis, "ND") and sex == 'MALE':
        target.append(0)
        df_new = df_new.append(row)
    if operator.contains(diagnosis, "MS") and sex == 'MALE':
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
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000910/results/ND_male_vs_MS_male_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['ND_male: ' + str("%.2f" % q2[0]), 'MS_male' + ": " + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'PLS-DA for ND_male verse MS_male')
##### End of Block 5: plsda for ND male verse MS male ################


##### Begin of Block 6: plsda for ND female verse MS female ################
df_new = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    diagnosis = df_factor[df_factor['local_sample_id'] == local_sample_id]['Diagnosis'].values[0]
    sex = df_factor[df_factor['local_sample_id'] == local_sample_id]['Sex'].values[0]

    if operator.contains(diagnosis, "ND") and sex == 'FEMALE':
        target.append(0)
        df_new = df_new.append(row)
    if operator.contains(diagnosis, "MS") and sex == 'FEMALE':
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
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000910/results/ND_female_vs_MS_female_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['ND_female: ' + str("%.2f" % q2[0]), 'MS_female' + ": " + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'PLS-DA for ND_female verse MS_female')
##### End of Block 6: plsda for ND female verse MS female ################


##### Begin of Block 7: plsda for MECFS verse MS ################
df_new = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    diagnosis = df_factor[df_factor['local_sample_id'] == local_sample_id]['Diagnosis'].values[0]
    sex = df_factor[df_factor['local_sample_id'] == local_sample_id]['Sex'].values[0]

    if operator.contains(diagnosis, "MECFS"):
        target.append(0)
        df_new = df_new.append(row)
    if operator.contains(diagnosis, "MS"):
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
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000910/results/MECFS_vs_MS_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['MECFS: ' + str("%.2f" % q2[0]), 'MS' + ": " + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'PLS-DA for MECFS verse MS')
##### End of Block 7: plsda for MECFS male verse MECFS female ################


##### Begin of Block 8: plsda for MECFS male verse MS male ################
df_new = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    diagnosis = df_factor[df_factor['local_sample_id'] == local_sample_id]['Diagnosis'].values[0]
    sex = df_factor[df_factor['local_sample_id'] == local_sample_id]['Sex'].values[0]

    if operator.contains(diagnosis, "MECFS") and sex == 'MALE':
        target.append(0)
        df_new = df_new.append(row)
    if operator.contains(diagnosis, "MS") and sex == 'MALE':
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
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000910/results/MECFS_male_vs_MS_male_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['MECFS_male: ' + str("%.2f" % q2[0]), 'MS_male' + ": " + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'PLS-DA for MECFS_male verse MS_male')
##### End of Block 8: plsda for MECFS male verse MS male ################


##### Begin of Block 9: plsda for MECFS female verse MS female ################
df_new = pd.DataFrame(columns=df_height_transposed.columns)
target = []
for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    diagnosis = df_factor[df_factor['local_sample_id'] == local_sample_id]['Diagnosis'].values[0]
    sex = df_factor[df_factor['local_sample_id'] == local_sample_id]['Sex'].values[0]

    if operator.contains(diagnosis, "MECFS") and sex == 'FEMALE':
        target.append(0)
        df_new = df_new.append(row)
    if operator.contains(diagnosis, "MS") and sex == 'FEMALE':
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
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000910/results/MECFS_female_vs_MS_female_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['MECFS_female: ' + str("%.2f" % q2[0]), 'MS_female' + ": " + str("%.2f" % q2[1])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target, target_names, 2, 'PLS-DA for MECFS_female verse MS_female')
##### End of Block 9: plsda for MECFS female verse MS female ################
