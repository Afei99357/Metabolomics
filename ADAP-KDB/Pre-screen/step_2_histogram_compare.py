import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()
# plt.clf()
# pd.set_option('precision', 15)
df = pd.read_csv("/Users/ericliao/PycharmProjects/phd_class_code/Lab_work/data_files/adap_kdb_algorithm_comparison/study_1110_spectra/time/8_15/prescreen_threshold_500_query_8_to_library_15_matches_combine.csv", header=0)

df_original_without_new_score = df[(df['Score Original'].notnull()) & (df['Score Prescreen'].isnull())]
df_original = df_original_without_new_score[['Score Original']]

df_both_scores = df[['Score Original', 'Score Prescreen']].dropna()

#
# n, bins, patched = plt.hist(df_original, bins=500, color='red', alpha=0.5)
# fig.suptitle('The original score without prescreen score', fontsize=10)
# plt.legend(['Score Original'])

df.sort_values(['Query Spectrum ID', "Score Original"], ascending=[True, False])
df['Rank'] = np.nan
query_spectrum_id = 0
count = 0

## REMEMBER TO CHANGE THE NUMBER IN range() for different msp file
for i in range(918):
    df.loc[df['Query Spectrum ID'] == i, 'Rank'] = range(1, 1 + len(df[df['Query Spectrum ID']==i]))
    df[df['Query Spectrum ID']==i]['Rank'] = range(1, 1 + len(df[df['Query Spectrum ID']==i]))

df.to_csv('/Users/ericliao/PycharmProjects/phd_class_code/Lab_work/data_files/adap_kdb_algorithm_comparison/study_1110_spectra/time/8_15/prescreen_threshold_500_query_8_to_library_15_matches_rank.csv')
df_rank = df.loc[df['Score Prescreen'].isnull(), 'Rank']
df_rank_100 = df_rank[df_rank < 100]
# n, bins, patched = plt.hist(df_rank_100, bins=150, color='red', alpha=0.5)
# fig.suptitle('Score Match Rank 0 - 100', fontsize=10)
# plt.legend(['Score Match Rank'])

colors = ['red', 'blue']
df_difference = df_both_scores["Score Original"] - df_both_scores["Score Prescreen"]
n, bins, patched = plt.hist(df_difference, bins=1000, color='red', alpha=0.5)
plt.legend(['Score Original', 'Score Prescreen'])

# fig, axes = plt.subplots(11, 11) #gridspec_kw={'width_ratios':[4,1,1,1,1,1,1,1,1,1,1], 'height_ratios':[4,4,4,4,4,4,4,4,4,4,4]}
# fig = plt.figure(figsize=(10, 10))

# n = 114
# colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
# column = 0
# row = 0
# for i, col in zip(range(114), colors):
#     fig = plt.figure(i)
#     df_new = df_original_without_new_score[df_original_without_new_score['Query Spectrum ID'] == i]
#     df_new_original = df_new[(df_new['Score Original'].notnull()) & (df_new['Score Prescreen'].isnull())]
#     df_original_plot = df_new_original[['Score Original']]
#     # n, bins, patched = plt.hist(df_original_plot, bins=10, color=col, alpha=0.5, ax=axes[row, column])
#     plt.hist(df_original_plot, bins=100, alpha=0.5, label=i, color=col)
#     # df_original_plot.hist('Score Original', bins=5, color=col, sharey=True, sharex=True)
#     if column < 11:
#         column = column + 1
#     if column >= 11:
#         column = 0
#         row = row + 1
#     fig.suptitle('original score -- query spectrum ' + str(i), fontsize=10)
#     plt.xlabel('similarity score')
#     plt.ylabel('counts')
#     fig.savefig("/Users/ericliao/Desktop/phD_courses/histgram_figs/" + str(i) + '.png')
##

##
# plt.yscale('log', nonposy='clip')
# plt.xscale('log')
# plt.xlabel('Rank Number')
plt.xlabel('Similarity Score')
plt.ylabel('counts')
# plt.title('Difference between the original and new scores when both scores exist')
# plt.title('Rank Counts')
# plt.tight_layout()
# plt.xticks(fontsize=1)
# plt.yticks(fontsize=1)
# plt.title(fontsize=1)
# plt.legend(loc='upper right')
plt.savefig("/Users/ericliao/PycharmProjects/phd_class_code/Lab_work/data_files/adap_kdb_algorithm_comparison/study_1110_spectra/time/8_15/1110_8_15_score_difference.png", dpi=300)

plt.show()