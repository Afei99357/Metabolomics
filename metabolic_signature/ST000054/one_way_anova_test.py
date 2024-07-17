import pandas as pd
from scipy.stats import f_oneway
from matplotlib import pyplot as plt
from statsmodels.sandbox.stats.multicomp import multipletests

df = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000054/data/aligned.csv', index_col=0)
df_factor = pd.read_csv('/Users/ericliao/Desktop/metabolomics_workbench_studies/ST000054/data/factors.csv')

df_all_information = df.loc[:, [' height' in i for i in df.columns]]
# df_all_information = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000054/original_height_data.csv', index_col=0)

df_significant_metabolites = pd.DataFrame(columns=df_all_information.columns)
pvalue_list = []



for index, item in df_all_information.iterrows():
    basal = []
    dcis = []
    her2 = []
    luma = []
    lumb = []
    reduction = []
    for x in item.index:
        local_sample_id = x.split(".", 1)[0]
        treatment_type = df_factor[df_factor['local_sample_id'] == local_sample_id]['treatment'].values[0]
        if not pd.isna(item[x]):
            if treatment_type.strip() == 'Basal':
                basal.append(item[x])
            if treatment_type.strip() == 'DCIS':
                dcis.append(item[x])
            if treatment_type.strip() == 'HER2':
                her2.append(item[x])
            if treatment_type.strip() == 'LumA':
                luma.append(item[x])
            if treatment_type.strip() == 'LumB':
                lumb.append(item[x])
            if treatment_type.strip() == 'Reduction':
                reduction.append(item[x])

    anova_result = f_oneway(basal, dcis, her2, luma, lumb, reduction)
    pvalue_list.append(anova_result.pvalue)


    if anova_result.pvalue < 0.05:
        df_significant_metabolites = df_significant_metabolites.append(df_all_information.iloc[index, :])


# Compute FDR using Benjamini-Hochberg procedure
fdrs = multipletests(pvalue_list, method = 'fdr_bh')[1]

plt.hist(pvalue_list)
plt.show()
df_significant_metabolites




