import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import operator

df_30min = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000965/results/0_min_vs_30_min.csv',
                       index_col=0)

df_60min = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000965/results/0_min_vs_60_min.csv',
                       index_col=0)

df_90min = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000965/results/0_min_vs_90_min.csv',
                       index_col=0)


df_factor = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000965/data/factors.csv')

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


df_30min = extract_height_df(df_30min)
df_60min = extract_height_df(df_60min)
df_90min = extract_height_df(df_90min)


common_columns = ['position', 'name', 'ms_level', 'polarity', 'retention_time', 'height', 'mz', 'neutral_mass',
                  'adducts', 'p_value', 'quantitation_mass']

df_part_1 = pd.merge(df_30min, df_60min, how='outer', on=common_columns, suffixes=('_30min', '_60min'))

df_part_2 = pd.merge(df_60min, df_90min, how='outer', on=common_columns, suffixes=('_60min', '_90min'))

df_new = pd.merge(df_part_1, df_part_2, how='outer', on=common_columns, suffixes=('', '_duplicate'))

df_new = df_new.drop(labels=[i for i in df_new.columns.tolist() if i.endswith('_duplicate')], axis=1)

# drop the rows that at least 2 of the columns(vip scores) is not na
df_ready = df_new.dropna(subset=['VIP_30min', 'VIP_60min', 'VIP_90min'], thresh=2)

df_ready = df_ready.fillna(0)


x = [1, 2, 3, 4]

all_heights_df = df_ready.loc[:, [' height_' in i for i in df_ready.columns]]

vips = df_ready.loc[:, ['VIP' in m for m in df_ready.columns]]

vips_copy = vips.copy()

vips_0min = np.zeros((vips.shape[0], 1))

vips_copy.insert(0, 'VIP_0min', vips_0min)

df_with_vips = pd.concat([all_heights_df, vips], axis=1)

new_index = 0
for index, item in df_with_vips.iloc[:, :-3].iterrows():
    y0 = []
    y1 = []
    y2 = []
    y3 = []
    for i in item.index:
        local_sample_id = i.split('.', 1)[0]
        group_info = df_factor[df_factor['local_sample_id'] == local_sample_id]['Treatment'].values[0]
        # get 0 hour information
        if operator.contains(group_info, "(0 min)") and i.endswith('_30min'):
            y0.append(item[i])
        # get other time course information
        if operator.contains(group_info, "(30 min)") and i.endswith('_30min'):
            y1.append(item[i])
        if operator.contains(group_info, "(60 min)") and i.endswith('_60min'):
            y2.append(item[i])
        if operator.contains(group_info, "(90 min)") and i.endswith('_90min'):
            y3.append(item[i])


    data = [y0, y1, y2 ,y3]


    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('time (min)')
    ax1.set_ylabel('Intensity')
    ax1.boxplot(data, positions=x)
    ax1.set_xticklabels(['0', '30', '60', '90'])
    # ax1.set_yscale('log')

    ax2 = ax1.twinx()
    ax2.set_ylabel('VIP', color=color)
    ax2.plot(x, vips_copy.iloc[new_index, :], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    metabolite_name = df_ready.iloc[new_index, 1:2]['name']
    plt.title(metabolite_name)

    plt.savefig('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000965/results/intensity_vip_plot/' + metabolite_name + '.png', dpi=300)

    new_index += 1
