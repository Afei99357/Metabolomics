import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/study_ST001190/'
                 'lung_vs_non_lung_st001190_vip_between_1_and_1.2.csv', index_col=False, sep=',')

height_columns = [col for col in df.columns if col.endswith(' height')]

df_height = df[[x for x in df.columns if x in height_columns]]

x_axis = ['Ileum', 'Jejunum', 'Liver', 'Lung', 'Skeletal Muscle']

df_ileum = df_height[[x for x in df_height.columns if x.startswith('I')]]
df_jejunum = df_height[[x for x in df_height.columns if x.startswith('J')]]
df_liver = df_height[[x for x in df_height.columns if x.startswith('Li')]]
df_lung = df_height[[x for x in df_height.columns if x.startswith('Lu')]]
df_skeletal_muscle = df_height[[x for x in df_height.columns if x.startswith('M')]]

for i in range(len(df)):
    # df_new
    df_new = pd.concat([df_ileum.loc[i, :], df_jejunum.loc[i, :], df_liver.loc[i, :],
                        df_lung.loc[i, :], df_skeletal_muscle.loc[i, :]], axis=1)
    df_new.plot.bar()
    plt.legend(labels=x_axis, loc='upper right')
    plt.savefig('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/study_ST001190/figures/intensity_figures/index_'
                + str(df.index[i]) + '.png')

