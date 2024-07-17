import pandas as pd
import operator
import statistics
from math import sqrt
from statsmodels.stats.power import TTestIndPower

df = pd.read_csv(
    "/Lab_work/data_files/metabolomics_signature/MTBLS196/Neg/between_different_organisms/with_feature_selection/"
    "vips_top10_annotated_organism.csv"
)

df_factor = pd.read_csv(
    "/Lab_work/data_files/metabolomics_signature/MTBLS196/Neg/MTBLS196_neg_factors.csv"
)

df_height = df.loc[:, [" height" in i for i in df.columns]]
df_height = df_height.fillna(0)

count_lung = 0
count_trachea = 0
lung_index_list = []
trachea_index_list = []

for i in df_height.columns.tolist():
    source_name = i.split(" ", 1)[0].strip()
    organism_part = df_factor[df_factor["Sample Name"] == source_name][
        "organism_part"
    ].values[0]

    if operator.contains(organism_part, "lung"):
        count_lung = count_lung + 1
        lung_index_list.append(True)
        trachea_index_list.append(False)

    if operator.contains(organism_part, "trachea"):
        count_trachea = count_trachea + 1
        lung_index_list.append(False)
        trachea_index_list.append(True)

number_of_lung, number_of_trachea = count_lung, count_trachea

### power analysis for each metabolite
for index, row in df_height.iterrows():
    ### variance of samples
    s_lung, s_trachea = statistics.variance(row[lung_index_list]), statistics.variance(
        trachea_index_list
    )

    ### calculate the pooled standard deviation
    ### (Cohen's d)
    s = sqrt(
        ((number_of_lung - 1) * s_lung + (number_of_trachea - 1) * s_trachea)
        / (number_of_lung + number_of_trachea - 2)
    )

    ### mean of samples
    mean_lung, mean_trachea = statistics.mean(row[lung_index_list]), statistics.mean(
        row[trachea_index_list]
    )

    ### calculate the effect size
    d = (mean_lung - mean_trachea) / s
    print(f"Effect size: {d}")

    ### factors for power analysis
    alpha = 0.05
    power = 0.8

    ### perform power analysis to find sample size
    ### for given effect
    obj = TTestIndPower()
    n = obj.solve_power(
        effect_size=d, alpha=alpha, power=power, ratio=1, alternative="two-sided"
    )

    print("Sample size/Number needed in each group: {:.3f}".format(n))
