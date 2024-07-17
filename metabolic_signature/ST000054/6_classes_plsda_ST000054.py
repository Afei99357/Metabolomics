import pandas as pd
import operator
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2

### modify 1
df = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000054/aligned.csv')
df_factor = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000054/factors.csv')

df_height = df.loc[:, [' height' in i for i in df.columns]]

df_height = df_height.fillna(0)

df_height_transposed = df_height.T

# df_new.to_csv("/Users/ericliao/Desktop/TEMP_TEST/ST000054/original_height_data.csv")
df_new = pd.DataFrame(columns=df_height_transposed.columns)


df_new['target'] = ''
target_color = []
target = []

for index, row in df_height_transposed.iterrows():
    local_sample_id = index.split(".", 1)[0]
    treatment_type = df_factor[df_factor['local_sample_id']==local_sample_id]['treatment'].values[0]
    pool_aliquot = df_factor[df_factor['local_sample_id']==local_sample_id]['pool aliquot'].values[0]
    if treatment_type.strip() == 'Basal' and pool_aliquot == 'no':
        target.append([1, 0, 0, 0, 0, 0])
        target_color.append(0)
        df_new = df_new.append(row)
        df_new.loc[index]['target'] = 0
    if treatment_type.strip() == 'DCIS' and pool_aliquot == 'no':
        target.append([0, 1, 0, 0, 0, 0])
        target_color.append(1)
        df_new = df_new.append(row)
        df_new.loc[index]['target'] = 1
    if treatment_type.strip() == 'HER2' and pool_aliquot == 'no':
        target.append([0, 0, 1, 0, 0, 0])
        target_color.append(2)
        df_new = df_new.append(row)
        df_new.loc[index]['target'] = 2
    if treatment_type.strip() == 'LumA' and pool_aliquot == 'no':
        target.append([0, 0, 0, 1, 0, 0])
        target_color.append(3)
        df_new = df_new.append(row)
        df_new.loc[index]['target'] = 3
    if treatment_type.strip() == 'LumB' and pool_aliquot == 'no':
        target.append([0, 0, 0, 0, 1, 0])
        target_color.append(4)
        df_new = df_new.append(row)
        df_new.loc[index]['target'] = 4
    if treatment_type.strip() == 'Reduction' and pool_aliquot == 'no':
        target.append([0, 0, 0, 0, 0, 1])
        target_color.append(5)
        df_new = df_new.append(row)
        df_new.loc[index]['target'] = 5


df_new.to_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000054/6_factors_height_data.csv')

### modify 2
target = np.array(target)

df_new = df_new.iloc[:, :-1]

plsr = pls_da_model.pls_da(df_new, target, 0)

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
df_out.to_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/studies/ST000054/'
              '6_classes_st000054_vip_greater_1.5_new_preprocess.csv')
#######################################################

######### print out the q2 with leave one out cross-validation #####
q2 = calculate_q2.calculate_q2(df_new, target, 6, 0)
####################################################################

######### scores: The scores describe the position of
### each sample in each determined latent variable (LV)####
scores = pd.DataFrame(plsr.x_scores_).to_numpy()
###############################################################

### modify 4
target_names = ['Basal: ' + str("%.2f" % q2[0]),
                'DCIS: ' + str("%.2f" % q2[1]),
                'HER2: ' + str("%.2f" % q2[2]),
                'LumA: ' + str("%.2f" % q2[3]),
                'LumB: ' + str("%.2f" % q2[4]),
                'Reduction: ' + str("%.2f" % q2[5])
                ]
target_names = np.array(target_names)

plot_2d.plsda_2d_plot(scores, target_color, target_names, 6)
