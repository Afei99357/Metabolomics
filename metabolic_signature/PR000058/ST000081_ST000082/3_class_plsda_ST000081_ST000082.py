import pandas as pd
import operator
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2

### load data
df_81_82 = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/PR000058/ST000081_ST000082/data/aligned.csv')
df_factor_81_82 = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/PR000058/ST000081_ST000082/data/factors.csv')

for index, item in df_factor_81_82.iterrows():
    item['local_sample_id'] = item['local_sample_id'].strip()

df_height_81_82 = df_81_82.loc[:, [' height' in i for i in df_81_82.columns]]
df_height_81_82 = df_height_81_82.fillna(0)

df_height_transposed_81_82 = df_height_81_82.T

##### Begin of Block 1: plsda################

df_new = pd.DataFrame(columns=df_height_transposed_81_82.columns)
target = []
target_color = []
sn=0
va=0
se=0
for index, row in df_height_transposed_81_82.iterrows():
    local_sample_id = index.split(".", 1)[0].strip()
    tissue_type = df_factor_81_82[df_factor_81_82['local_sample_id'] == local_sample_id]['Tissue type'].values[0]

    if operator.contains(tissue_type, "Subcutaenous Adipose"):
        target.append([1, 0, 0])
        df_new = df_new.append(row)
        target_color.append(0)
        sn = sn+1
    if operator.contains(tissue_type, "Visceral Adipose"):
        target.append([0, 1, 0])
        df_new = df_new.append(row)
        target_color.append(1)
        va = va + 1
    if operator.contains(tissue_type, "Serum"):
        target.append([0, 0, 1])
        df_new = df_new.append(row)
        target_color.append(2)
        se = se + 1

target = np.array(target)

plsr = pls_da_model.pls_da(df_new, target, 0)

########## calculate VIPs vector ######################
vip_value = vips.vips(plsr)

vip_index = np.argsort(vip_value)

df_out = pd.DataFrame(columns=df_81_82.columns)
df_out['VIP'] = None

n_index = 0
for i in vip_index:
    if vip_value[i] >= 0:
        df_out = df_out.append(df_81_82.iloc[i])
        df_out['VIP'].iloc[n_index] = vip_value[i]
        n_index += 1


## output metabolites vip score
df_out.to_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/PR000058/ST000081_ST000082/results/SubcutaenousAdipose_vs_VisceralAdipose_vs_serum_vip_gretaer_0.csv')
######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 3, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### plot plsda
target_names = ['Subcutaenous Adipose Q2: ' + str("%.2f" % q2[0]), 'Visceral Adipose Q2' + ": " + str("%.2f" % q2[1]), 'Serum Q2' + ": " + str("%.2f" % q2[2])]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target_color, target_names, 3, 'PLS-DA for Subcutaenous Adipose, Visceral Adipose and Serum')
##### End of Block 1: plsda ################