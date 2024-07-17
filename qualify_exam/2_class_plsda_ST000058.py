import pandas as pd
import operator
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2

### modify 1
df = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000058/data/aligned.csv')
df_factor = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000058/data/factors.csv')

for index, item in df_factor.iterrows():
    item['local_sample_id'] = item['local_sample_id'].strip()

df_height = df.loc[:, [' height' in i for i in df.columns]]
df_height = df_height.fillna(0)
df_height_transposed = df_height.T

groups = ['Group 2', 'Group 3', 'Group 4', 'Group 5', 'Group 6', 'Group 7']
time_course = ['2_hours', '4_hours', '8_hours', '12_hours', '24_hours', '48_hours']


for group, time in zip(groups, time_course):
    df_new = pd.DataFrame(columns=df_height_transposed.columns)
    df_new['target'] = ''
    target = []

    for index, row in df_height_transposed.iterrows():
        local_sample_id = index.split(".", 1)[0].strip()

        treatment_type = df_factor[df_factor['local_sample_id']==local_sample_id]['Treatment'].values[0]

        if operator.contains(treatment_type, "Methionine"):
            target.append(0)
            df_new = df_new.append(row)
            df_new.loc[index]['target'] = 0
        if operator.contains(treatment_type, "Homocysteine"):
            if treatment_type.endswith(group):
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


    ### output metabolites vip score
    # df_out.to_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000058/0_hour_vs_' + time + '_st000058_vip_greater_0.csv')
    #######################################################

    ######### print out the q2 with leave one out cross-validation #####
    q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
    ####################################################################

    ######### scores: The scores describe the position of
    ### each sample in each determined latent variable (LV)####
    scores = pd.DataFrame(plsr.x_scores_).to_numpy()
    ###############################################################

    ### modify 4
    target_names = ['0_hours: ' + str("%.2f" % q2[0]), time + ": " + str("%.2f" % q2[1])]
    target_names = np.array(target_names)

    plot_2d.plsda_2d_plot(scores, target, target_names, 2)
