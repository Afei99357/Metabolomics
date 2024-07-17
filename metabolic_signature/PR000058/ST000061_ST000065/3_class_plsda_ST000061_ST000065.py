import pandas as pd
import operator
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2

### load data
df_61_65 = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/PR000058/ST000061_ST000065/data/aligned.csv')
df_factor_61_65 = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/PR000058/ST000061_ST000065/data/factors.csv')

for index, item in df_factor_61_65.iterrows():
    item['local_sample_id'] = item['local_sample_id'].strip()


df_height_61_65 = df_61_65.loc[:, [' height' in i for i in df_61_65.columns]]
df_height_61_65 = df_height_61_65.fillna(0)
df_height_transposed_61 = df_height_61_65.T

##### Begin of Block 1: plsda################

df_new = pd.DataFrame(columns=df_height_transposed_61.columns)
target = []
target_color = []
for index, row in df_height_transposed_61.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    label = df_factor_61_65[df_factor_61_65['local_sample_id'] == local_sample_id]['Source'].values[0]

    if operator.contains(label, "Subcutaenous Fat"):
        target.append([1, 0, 0])
        df_new = df_new.append(row)
        target_color.append(0)
    if operator.contains(label, "Visceral Fat"):
        target.append([0, 1, 0])
        df_new = df_new.append(row)
        target_color.append(1)
    if operator.contains(label, "Serum"):
        target.append([0, 0, 1])
        df_new = df_new.append(row)
        target_color.append(2)

target = np.array(target)

plsr = pls_da_model.pls_da(df_new, target, 0)

########## calculate VIPs vector ######################
vip_value = vips.vips(plsr)

vip_index = np.argsort(vip_value)

df_out = pd.DataFrame(columns=df_61_65.columns)
df_out['VIP'] = None

n_index = 0
for i in vip_index:
    if vip_value[i] >= 0:
        df_out = df_out.append(df_61_65.iloc[i])
        df_out['VIP'].iloc[n_index] = vip_value[i]
        n_index += 1


## output metabolites vip score
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/PR000058/ST000061_ST000065/results/SubcutaenousFat_vs_VisceralFat_vs_Serum_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 3, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['Subcutaenous Fat Q2: ' + str("%.2f" % q2[0]), 'Visceral Fat Q2' + ": " + str("%.2f" % q2[1]), 'Serum Q2' + ": " + str("%.2f" % q2[2])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target_color, target_names, 3, 'PLS-DA for Subcutaenous Fat, Visceral Fat and Serum')
##### End of Block 1: plsda ################