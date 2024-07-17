import pandas as pd
import matplotlib.pyplot as plt
from venn import pseudovenn
from venn import venn

df = pd.read_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/POS/"
    "new_analysis/with_feature_selection/vips_annotated.csv",
    index_col=0,
    header=0,
)

df_fdr_5 = pd.read_csv("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1033/"
                       "Urine/POS/new_analysis/R_STUDIO/pvalue_significant_index_fdr_5_percent.csv", header=0)

fdr_5 = df_fdr_5["x"].tolist()
fdr_5_new = [i-1 for i in fdr_5]

VIP_greater_1 = df[df["VIP"] > 1].index.tolist()


fdr_set = set(fdr_5_new)

vip_top_150_set = set(VIP_greater_1)


labels = ["FDR under 5%", "VIP greater than 1"]

sets = {labels[0]: fdr_set, labels[1]: vip_top_150_set}

fig, ax = plt.subplots(1, figsize=(10, 10))
venn(sets, ax=ax)
plt.legend(labels[:], ncol=2)
plt.show()


def intersection(list1, list2):
    list3 = [value for value in list1 if value in list2]
    return list3

def different(list1, list2):
    list3 = [value for value in list1 if value not in list2]
    return list3

overlap_fdr_5_vip_1 = intersection(fdr_5_new, vip_top_150_set)
print(overlap_fdr_5_vip_1)
print(len(overlap_fdr_5_vip_1))
print(different(fdr_5_new, vip_top_150_set))
