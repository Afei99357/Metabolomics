import pandas as pd
import matplotlib.pyplot as plt
from venn import pseudovenn
from venn import venn

df = pd.read_csv('/Users/ericliao/Desktop/anova_vs_vip_results.csv', index_col=None,header=0)

fdr_5 = df['pvalue_fdr_5_percent'].tolist()
fdr_10 = df['pvalue_fdr_10_percent'].tolist()
vip_greater_1_5 = df['vip_greater_1.5'].tolist()
vip_greater_1_3 = df['vip_greater_1.3'].tolist()

fdr_5_set = set(fdr_5)
fdr_10_set = set(fdr_10)
vip_greater_1_5_set = set(vip_greater_1_5)
vip_greater_1_3_set = set(vip_greater_1_3)

labels = ['FDR under 5%', 'FDR under 10%', "VIP greater than 1.5", "VIP greater than 1.3"]

sets = {labels[0]: fdr_5_set,
        labels[1]: fdr_10_set,
        labels[2]: vip_greater_1_5_set,
        labels[3]: vip_greater_1_3_set}

fig, ax = plt.subplots(1, figsize=(10, 10))
venn(sets, ax=ax)
plt.legend(labels[:], ncol=4)
plt.show()

def intersection(list1, list2):
    list3 = [value for value in list1 if value in list2]
    return list3

overlap_fdr5_vip_1_5 = intersection(fdr_5, vip_greater_1_5)
print(overlap_fdr5_vip_1_5)
print(len(overlap_fdr5_vip_1_5))

overlap_fdr10_vip_1_3 = intersection(fdr_10, vip_greater_1_3)
print(overlap_fdr10_vip_1_3)
print(len(overlap_fdr10_vip_1_3))



