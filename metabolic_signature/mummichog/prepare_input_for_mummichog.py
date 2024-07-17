import pandas as pd
import operator
from scipy.stats import f_oneway
from statsmodels.sandbox.stats.multicomp import multipletests

df_original = pd.read_csv("/Users/ericliao/Desktop/metabolomics_workbench_studies/"
                          "PR000058/ST000081_ST000082/data/aligned.csv")
df_factor = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/PR000058/'
                        'ST000081_ST000082/data/factors.csv')

# get quantitative data
df_height = df_original.loc[:, [' height' in i for i in df_original.columns]]

df_height.drop('Pooled MSMS.mzXML height', inplace=True, axis=1)

df_height = df_height.dropna(axis=0, how='all')

df_height = df_height.fillna(0)

pvalue_list = []
f_score_list = []

for index, item in df_height.iterrows():
    serum_group = []
    subcutaenous_group = []
    visceral_group = []
    for x in item.index:
        local_sample_id = x.split(".", 1)[0]
        source_type = df_factor[df_factor['local_sample_id'] == local_sample_id]['Tissue type'].values[0]
        if not pd.isna(item[x]):
            if operator.contains(source_type, "Serum"):
                serum_group.append(item[x])
            if operator.contains(source_type, "Subcutaenous"):
                subcutaenous_group.append(item[x])
            if operator.contains(source_type, "Visceral"):
                visceral_group.append(item[x])

    anova_result = f_oneway(serum_group, subcutaenous_group, visceral_group)
    pvalue_list.append(anova_result.pvalue)
    f_score_list.append(anova_result.statistic)


# Compute FDR using Benjamini-Hochberg procedure
fdrs = multipletests(pvalue_list, method='fdr_bh')[1]

df_output = pd.DataFrame(columns=['m/z', 'retention_time', 'p-value', 'f-score', 'FDR_BH', 'custom_id'])
df_output_statistic = pd.DataFrame(columns=['m/z', 'retention_time', 'p-value', 'f-score'])

new_index = 0
for index, item in df_height.iterrows():

    original_item = df_original.iloc[index, :]

    row_dict = {"m/z": original_item['mz'], "retention_time": original_item["retention_time"], "p-value": pvalue_list[new_index],
                'f-score': f_score_list[new_index], "FDR_BH": fdrs[new_index], "custom_id": original_item["position"]}
    df_output = df_output.append(row_dict, ignore_index=True)

    row_2_dict = {"m/z": original_item['mz'], "retention_time": original_item["retention_time"], "p-value": pvalue_list[new_index],
                'f-score': f_score_list[new_index]}
    df_output_statistic = df_output_statistic.append(row_2_dict, ignore_index=True)

    new_index = new_index + 1


df_output.to_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/'
                 'metabolomics_signature/mummichog/mummichog_input_st000081_st000082.csv', sep='\t')


df_output_statistic.to_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/'
                 'metabolomics_signature/mummichog/mummichog_statistics_st000081_st000082.csv', sep='\t')