import pandas as pd
import operator
import statistics
from math import sqrt
from statsmodels.stats.power import TTestIndPower
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning

warnings.simplefilter('ignore', ConvergenceWarning)

df = pd.read_csv(
    "/Lab_work/data_files/metabolic_signature/MTBLS196/Neg/between_virus/with_feature_selection/trachea/vips_top10_annotated_trachea_virus.csv"
)
df_factor = pd.read_csv(
    "/Lab_work/data_files/metabolic_signature/MTBLS196/Neg/"
    "MTBLS196_neg_factors.csv"
)

df_height = df.loc[:, [" height" in i for i in df.columns]]
df_height = df_height.fillna(0)

count_lung = 0
count_trachea = 0
virus_1918_index_list = []
virus_Cal04RG_index_list = []

for i in df_height.columns.tolist():
    source_name = i.split(" ", 1)[0].strip()
    organism_part = df_factor[df_factor["Sample Name"] == source_name][
        "organism_part"
    ].values[0]
    virus_type = df_factor[df_factor["Sample Name"] == source_name]["virus"].values[0]

    if operator.contains(organism_part, "trachea") and operator.contains(virus_type, "1918"):
        count_lung = count_lung + 1
        virus_1918_index_list.append(True)
        virus_Cal04RG_index_list.append(False)

    if operator.contains(organism_part, "trachea") and operator.contains(virus_type, "Cal04RG"):
        count_trachea = count_trachea + 1
        virus_1918_index_list.append(False)
        virus_Cal04RG_index_list.append(True)

    if operator.contains(virus_type, "mock") or operator.contains(organism_part, "lung"):
        virus_1918_index_list.append(False)
        virus_Cal04RG_index_list.append(False)

number_of_lung, number_of_trachea = count_lung, count_trachea

### power analysis for each metabolite
for index, row in df_height.iterrows():
    ### variance of samples
    s_lung = statistics.variance(row[virus_1918_index_list])
    s_trachea = statistics.variance(virus_Cal04RG_index_list)

    ### calculate the pooled standard deviation
    ### (Cohen's d)
    s = sqrt(
        ((number_of_lung - 1) * s_lung + (number_of_trachea - 1) * s_trachea)
        / (number_of_lung + number_of_trachea - 2)
    )

    ### mean of samples
    mean_virus_1918 = statistics.mean(row[virus_1918_index_list])
    mean_virus_Cal04RG = statistics.mean(row[virus_Cal04RG_index_list])

    ### calculate the effect size
    d = (mean_virus_1918 - mean_virus_Cal04RG) / s
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

    if type(n) != float:

        print("Cannot find a solution for this feature!")
        continue

    print("Sample size/Number needed in each group: {:.3f}".format(n))



