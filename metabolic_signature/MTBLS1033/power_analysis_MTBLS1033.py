#### Power analysis: https://www.geeksforgeeks.org/introduction-to-power-analysis-in-python/

import pandas as pd
import operator
import statistics
from math import sqrt
from statsmodels.stats.power import TTestIndPower

df = pd.read_csv(
    "/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/"
    "NEG/with_feature_selection/vips_top10_annotated.csv"
)

df_factor = pd.read_csv(
    "/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/NEG/MTBLS1033_factors.csv"
)

df_height = df.loc[:, [" height" in i for i in df.columns]]
df_height = df_height.fillna(0)

count_pop = 0
count_control = 0
pop_index_list = []
control_index_list = []
pop_control_index = []

for i in df_height.columns.tolist():
    source_name = i.split(" ", 1)[0].strip()
    organism_part = df_factor[df_factor["Source Name"] == source_name][
        "Factor Value[Group]"
    ].values[0]

    if operator.contains(organism_part, "POP"):
        count_pop = count_pop + 1
        pop_index_list.append(True)
        control_index_list.append(False)
        pop_control_index.append(True)

    if operator.contains(organism_part, "Control"):
        count_control = count_control + 1
        pop_index_list.append(False)
        control_index_list.append(True)
        pop_control_index.append(True)

    if operator.contains(organism_part, "Quality control"):
        pop_control_index.append(False)

number_of_pop, number_of_control = count_pop, count_control

df_height_new = df_height.loc[:, pop_control_index]

for index, row in df_height_new.iterrows():
    ### variance of samples
    s_pop, s_control = statistics.variance(row[pop_index_list]), statistics.variance(
        control_index_list
    )

    ### calculate the pooled standard deviation
    ### (Cohen's d)
    s = sqrt(
        ((number_of_pop - 1) * s_pop + (number_of_control - 1) * s_control)
        / (number_of_pop + number_of_control - 2)
    )

    ### mean of samples
    mean_pop, mean_control = statistics.mean(row[pop_index_list]), statistics.mean(
        row[control_index_list]
    )

    ### calculate the effect size
    d = (mean_pop - mean_control) / s
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
