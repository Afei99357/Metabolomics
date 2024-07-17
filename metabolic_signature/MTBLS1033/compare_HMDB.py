import pandas as pd
import matplotlib.pyplot as plt
from venn import venn


mtbls1033_urine_pos_df = pd.read_csv('/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/POS/matched_new.csv')

mtbls1033_urine_neg_df = pd.read_csv('/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/NEG/matched_new.csv')

hmdb_urine_df = pd.read_csv('/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/HMDB_sample_files/csv_files/urine_metabolites.csv', header=0, index_col=False)

mtbls1033_urine_pos_set = set(mtbls1033_urine_pos_df["InChIKey"].tolist())

mtbls1033_urine_neg_set = set(mtbls1033_urine_neg_df["InChIKey"].tolist())

hmdb_urine_set = set(hmdb_urine_df['inchikey'])

labels = ['MTBLS1033 Urine pos', 'MTBLS1033 Urine neg', 'HMDB Urine']

def intersection(list1, list2):
    list3 = [value for value in list1 if value in list2]
    return list3

overlap_pos_hmdb = intersection(mtbls1033_urine_pos_set, hmdb_urine_set)
overlap_neg_hmdb = intersection(mtbls1033_urine_neg_set, hmdb_urine_set)
three_way_overlap = intersection(overlap_pos_hmdb, overlap_neg_hmdb)

print(len(overlap_pos_hmdb))
print(len(overlap_neg_hmdb))
print(len(three_way_overlap))

sets = {
    labels[0]: mtbls1033_urine_pos_set,
    labels[1]: mtbls1033_urine_neg_set,
    labels[2]: hmdb_urine_set
}

fig, ax = plt.subplots(1, figsize=(10, 10))
venn(sets, ax=ax)
plt.legend(labels[:], ncol=3)
plt.show()

## todo: output the overlapping compounds in pos and neg mode. check the VIPs in different mode.

