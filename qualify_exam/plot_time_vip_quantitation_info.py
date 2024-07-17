import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import operator

df_2hour = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000058_new/results/0_hour_vs_2_hours_st000058_vip_greater_0.csv',
                       index_col=0)

df_4hour = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000058_new/results/0_hour_vs_4_hours_st000058_vip_greater_0.csv',
                       index_col=0)

df_8hour = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000058_new/results/0_hour_vs_8_hours_st000058_vip_greater_0.csv',
                       index_col=0)

df_12hour = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000058_new/results/0_hour_vs_12_hours_st000058_vip_greater_0.csv',
                        index_col=0)

df_24hour = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000058_new/results/0_hour_vs_24_hours_st000058_vip_greater_0.csv',
                        index_col=0)

df_48hour = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000058_new/results/0_hour_vs_48_hours_st000058_vip_greater_0.csv',
                        index_col=0)

df_factor = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000058_new/data/factors.csv')

for index, item in df_factor.iterrows():
    item['local_sample_id'] = item['local_sample_id'].strip()

"""
To extract the metabolits basic infor, sample height and vip information 
"""


def extract_height_df(df):
    df_head = df.loc[:, "position": "quantitation_mass"]

    df_height = df.loc[:, [' height' in i for i in df.columns]]

    df_height = df_height.fillna(0)

    df_combine = pd.concat([df_head, df_height], axis=1)

    df_output = pd.concat([df_combine, df['VIP']], axis=1)

    return df_output


df_2hour = extract_height_df(df_2hour)
df_4hour = extract_height_df(df_4hour)
df_8hour = extract_height_df(df_8hour)
df_12hour = extract_height_df(df_12hour)
df_24hour = extract_height_df(df_24hour)
df_48hour = extract_height_df(df_48hour)

common_columns = ['position', 'name', 'ms_level', 'polarity', 'retention_time', 'height', 'mz', 'neutral_mass',
                  'adducts', 'p_value', 'quantitation_mass']

df_part_1 = pd.merge(df_2hour, df_4hour, how='outer', on=common_columns, suffixes=('_2hour', '_4hour'))

df_part_2 = pd.merge(df_8hour, df_12hour, how='outer', on=common_columns, suffixes=('_8hour', '_12hour'))

df_part_3 = pd.merge(df_24hour, df_48hour, how='outer', on=common_columns, suffixes=('_24hour', '_48hour'))

df_new = pd.merge(df_part_1, df_part_2, how='outer', on=common_columns)

df_new = pd.merge(df_new, df_part_3, how='outer', on=common_columns)

# drop the rows that at least 5 of the columns(vip scores) is not na
df_ready = df_new.dropna(subset=['VIP_2hour', 'VIP_4hour', 'VIP_8hour', 'VIP_12hour', 'VIP_24hour', 'VIP_48hour'],
                         thresh=5)

df_ready = df_ready.fillna(0)

# df_ready.to_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/studies/ST000058/'
#                 'new_process/vip_greater_than_1_at_most_1_is_na.csv')

x = [1, 2, 3, 4, 5, 6, 7]

all_heights_df = df_ready.loc[:, [' height_' in i for i in df_ready.columns]]

vips = df_ready.loc[:, ['VIP' in m for m in df_ready.columns]]

vips_copy = vips.copy()

vips0hour = np.zeros((vips.shape[0], 1))

vips_copy.insert(0, 'VIP0hour', vips0hour)

df_with_vips = pd.concat([all_heights_df, vips], axis=1)

new_index = 0
for index, item in df_with_vips.iloc[:, :-6].iterrows():
    y = np.empty((7, 4))
    y0 = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    y6 = []
    for i in item.index:
        local_sample_id = i.split('.', 1)[0]
        group_info = df_factor[df_factor['local_sample_id'] == local_sample_id]['Treatment'].values[0]
        # get 0 hour information
        if operator.contains(group_info, "Group 1") and i.endswith('_2hour'):
            y0.append(item[i])

        # get other time course information
        if operator.contains(group_info, "Group 2") and i.endswith('_2hour'):
            y1.append(item[i])
        if operator.contains(group_info, "Group 3") and i.endswith('_4hour'):
            y2.append(item[i])
        if operator.contains(group_info, "Group 4") and i.endswith('_8hour'):
            y3.append(item[i])
        if operator.contains(group_info, "Group 5") and i.endswith('_12hour'):
            y4.append(item[i])
        if operator.contains(group_info, "Group 6") and i.endswith('_24hour'):
            y5.append(item[i])
        if operator.contains(group_info, "Group 7") and i.endswith('_48hour'):
            y6.append(item[i])

    y[0] = y0
    y[1] = y1
    y[2] = y2
    y[3] = y3
    y[4] = y4
    y[5] = y5
    y[6] = y6

    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('time (min)')
    ax1.set_ylabel('Intensity')
    ax1.boxplot(y.T, positions=x)
    ax1.set_xticklabels(['0', '2', '4', '8', '12', '24', '48'])
    # ax1.set_yscale('log')

    ax2 = ax1.twinx()
    ax2.set_ylabel('VIP', color=color)
    ax2.plot(x, vips_copy.iloc[new_index, :], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    metabolite_name = df_ready.iloc[new_index, 1:2]['name']
    plt.title(metabolite_name)

    plt.savefig('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000058_new/results/vip_intensity_plot/' + metabolite_name + '.png', dpi=300)

    new_index += 1
