import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/study_ST000574/'
                 'muscle+heart_vs_non_muscle+heart_metabolites_st000574_vip_between_1_and_1dot2.csv', index_col=False, sep=',')

height_columns = [col for col in df.columns if col.endswith('CDF height')]

df_height = df[[x for x in df.columns if x in height_columns]]

x_axis = ['Heart', 'Muscle', 'Liver', 'Serum']

df_heart_muscle = df_height[[x for x in df_height.columns if x.startswith('H') or x.startswith('M')]]

df_heart = df_height[[x for x in df_height.columns if x.startswith('H')]]
df_muscle = df_height[[x for x in df_height.columns if x.startswith('M')]]
df_liver = df_height[[x for x in df_height.columns if x.startswith('L')]]
df_serum = df_height[[x for x in df_height.columns if x.startswith('S')]]

for i in range(len(df_heart_muscle)):
    # df_new = pd.concat([df_heart_muscle.loc[i, :], df_liver.loc[i, :], df_serum.loc[i, :]], axis=1)
    df_new = pd.concat([df_heart.loc[i, :], df_muscle.loc[i, :], df_liver.loc[i, :], df_serum.loc[i, :]], axis=1)
    # df_new.set_axis(x_axis, axis=1)
    df_new.plot.bar()
    plt.legend(labels=x_axis, loc='upper right')
    plt.savefig('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/study_ST000574/figures/intensity_figures/index_'
                + str(df.index[i]) + '.png')

# y_axis = np.zeros((3, 2))
