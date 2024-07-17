import pandas as pd
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2

### loading raw data and factors
df = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000054/data/aligned.csv')
df_factor = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000054/data/factors.csv')

# get quantitative data
df_height = df.loc[:, [' height' in i for i in df.columns]]

df_height = df_height.fillna(0)

df_height_transposed = df_height.T

# get different fators
cancer_stages = ['Basal', 'DCIS', 'HER2', 'LumA', 'LumB']

# loop through each stage and perform PLS-DA against normal cell (Reduction)
for item in cancer_stages:
    df_new = pd.DataFrame(columns=df_height_transposed.columns)
    df_new['target'] = ''
    target = []
    # according to each stage to get the corresponding data and the target
    for index, row in df_height_transposed.iterrows():
        local_sample_id = index.split(".", 1)[0]
        treatment_type = df_factor[df_factor['local_sample_id']==local_sample_id]['treatment'].values[0]
        pool_aliquot = df_factor[df_factor['local_sample_id']==local_sample_id]['pool aliquot'].values[0]

        if treatment_type.strip() == 'Reduction':
            target.append(0)
            df_new = df_new.append(row)
            df_new.loc[index]['target'] = 0
        if treatment_type.strip() != item:
            target.append(1)
            df_new = df_new.append(row)
            df_new.loc[index]['target'] = 1

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
        if vip_value[i] >= 0:
            df_out = df_out.append(df.iloc[i])
            df_out['VIP'].iloc[n_index] = vip_value[i]
            n_index += 1


    ## modify 3
    # df_out.to_csv('./ST000054/'+ str(item) +'_vs_Non_' + str(item)+'_st000054_vips_greater_0.csv')
    ######################################################

    ######### print out the q2 with leave one out cross-validation #####
    q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
    ####################################################################

    ######### scores: The scores describe the position of
    ### each sample in each determined latent variable (LV)####
    scores = pd.DataFrame(plsr.x_scores_).to_numpy()
    ###############################################################

    ### PLS-DA plot
    target_names = ['Reduction: ' + str("%.2f" % q2[0]), item+": " + str("%.2f" % q2[1])]
    target_names = np.array(target_names)

    plot_2d.plsda_2d_plot(scores, target, target_names, 2)
