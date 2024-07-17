import pandas as pd
import matplotlib.pyplot as plt
from venn import venn


##### all compounds
df_ga_tech = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/consortium_lipid_data_new/'
                         'VIP_results/GaTech_vip_greater_1.9.csv',
                         header=0, index_col=False)

df_umich = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/consortium_lipid_data_new/'
                       'VIP_results/UMich_vip_greater_1.9_edit.csv',
                       header=0, index_col=False)

df_ucd = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/consortium_lipid_data_new/'
                     'VIP_results/UCD_vip_greater_1.9_edit.csv',
                     header=0, index_col=False)

df_ucd_qtof = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/consortium_lipid_data_new/'
                          'VIP_results/UCD_qToF_vip_greater_1.9'
                          '_edit.csv',
                          header=0, index_col=False)

df_original = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/consortium_lipid_data_new/'
                          'original_lipids.csv',
                          header=0, index_col=False)


##### all unknown compounds
df_ga_tech_unknown = df_ga_tech[(df_ga_tech['Metabolite name'] == 'Unknown')
                                + (df_ga_tech['Metabolite name'].str.startswith('RIKEN'))
                                + (df_ga_tech['Metabolite name'].str.startswith('w/o MS2'))]

df_umich_unknown = df_umich[(df_umich['Metabolite name'] == 'Unknown')
                            + (df_umich['Metabolite name'].str.startswith('RIKEN'))
                            + (df_umich['Metabolite name'].str.startswith('w/o MS2'))]

df_ucd_unknown = df_ucd[(df_ucd['Metabolite name'] == 'Unknown')
                        + (df_ucd['Metabolite name'].str.startswith('RIKEN'))
                        + (df_ucd['Metabolite name'].str.startswith('w/o MS2'))]

df_ucd_qtof_unknown = df_ucd_qtof[(df_ucd_qtof['Metabolite name'] == 'Unknown')
                                  + (df_ucd_qtof['Metabolite name'].str.startswith('RIKEN'))
                                  + (df_ucd_qtof['Metabolite name'].str.startswith('w/o MS2'))]

# df_original.reset_index()


##### all compound
# set1 = set(df_ga_tech.iloc[:, 0].tolist())
# set2 = set(df_umich.iloc[:, 0].tolist())
# set3 = set(df_ucd.iloc[:, 0].tolist())
# set4 = set(df_ucd_qtof.iloc[:, 0].tolist())

#### unknown compound
set1 = set(df_ga_tech_unknown.iloc[:, 0].tolist())
set2 = set(df_umich_unknown.iloc[:, 0].tolist())
set3 = set(df_ucd_unknown.iloc[:, 0].tolist())
set4 = set(df_ucd_qtof_unknown.iloc[:, 0].tolist())

set_intersection = set1.intersection(set2.intersection(set3.intersection(set4)))

df_common = df_original.iloc[list(set_intersection)]

df_common.to_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/consortium_lipid_data_new/'
                 'overlap_unknown_compounds_vip_1.9.csv')

print(len(set_intersection))

labels = ['GaTech', 'UMich', 'UCD', 'UCD qToF']

sets = {
    labels[0]: set1,
    labels[1]: set2,
    labels[2]: set3,
    labels[3]: set4
}

fig, ax = plt.subplots(1, figsize=(10, 10))
# pseudovenn(sets, ax=ax)
venn(sets, ax=ax)
# pseudovenn(sets, fmt='{percentage:.1f}%', ax=ax)
plt.legend(labels[:], ncol=6)

plt.show()
