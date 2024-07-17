import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.sandbox.stats.multicomp import multipletests
import numpy as np

#### load align.csv and factor file
df_original = pd.read_csv(
    "/Lab_work/data_files/metabolic_signature/MTBLS196/Neg/aligned.csv"
)
df_factor = pd.read_csv(
    "/Lab_work/data_files/metabolic_signature/MTBLS196/Neg/MTBLS196_neg_factors.csv"
)

#### create a dictionary for sample name and sample class
factor_map_dic = dict(zip(df_factor["Sample Name"], df_factor["organism_part"]))

### reference for other methods to crate the dictionary
# factor_map_dic = dict((df_factor["Source Name"].iloc[i] , df_factor["Factor Value[Group]"].iloc[i]) for i in range(len(df_factor)))
# factor_map_dic = {df_factor["Source Name"].iloc[i] : df_factor["Factor Value[Group]"].iloc[i] for i in range(len(df_factor))}

# get quantitative data
df_height = df_original.loc[:, [" height" in i for i in df_original.columns]]

# df_height.drop('Pooled MSMS.mzXML height', inplace=True, axis=1)

df_height = df_height.dropna(axis=0, how="all")

df_height = df_height.fillna(0)

#### get all the file names/sample names from the aligned.csv corresponding to the sample names in factor files
column_name_list = [x.split(" ", 1)[0].strip() for x in df_height.columns]


#### get the lung samples columns from the original dataframe: df_height
df_lung = df_height[
    [
        original_name
        for modify_name, original_name in zip(column_name_list, df_height.columns)
        if factor_map_dic[modify_name] == "lung"
    ]
]

#### get the trachea samples columns from the original dataframe: df_height
df_trachea = df_height[
    [
        original_name
        for modify_name, original_name in zip(column_name_list, df_height.columns)
        if factor_map_dic[modify_name] == "trachea"
    ]
]

#### do t-test for each metabolite
t_stat_list, pvalue_list = ttest_ind(df_lung.values, df_trachea.values, axis=1)

#### Compute FDR using Benjamini-Hochberg procedure
fdrs = multipletests(pvalue_list, method="fdr_bh")[1]

df_output_list = []
df_ouput_statistic_list = []

#### create the tables for mummichog
new_index = 0
for index, item in df_height.iterrows():
    original_item = df_original.iloc[index, :]

    row_dict = {
        "m/z": original_item["mz"],
        "retention_time": original_item["retention_time"],
        "p-value": pvalue_list[new_index],
        "t-stat": t_stat_list[new_index],
        "FDR_BH": fdrs[new_index],
        "custom_id": original_item["position"],
    }

    row_2_dict = {
        "m/z": original_item["mz"],
        "retention_time": original_item["retention_time"],
        "p-value": pvalue_list[new_index],
        "t-stat": t_stat_list[new_index],
    }

    df_ouput_statistic_list.append(row_dict)
    df_output_list.append(row_2_dict)

    new_index = new_index + 1

df_output = pd.DataFrame.from_dict(df_output_list)
df_output_statistic = pd.DataFrame.from_dict(df_ouput_statistic_list)

#### remove empty p-value and t-stat
df_output = df_output.dropna(subset=["p-value", "t-stat"])
# df_output = df_output.fillna(value=np.nan)

#### output the files
df_output.to_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolomics_signature/MTBLS196/Neg/mummichog/mummichog_input_mtbls196_neg.csv",
    sep="\t",
)

df_output_statistic.to_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolomics_signature/MTBLS196/Neg/mummichog/mummichog_statistics_mtbls196_neg.csv",
    sep="\t",
)
