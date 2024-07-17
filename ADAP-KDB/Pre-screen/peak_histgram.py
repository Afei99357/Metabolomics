import pandas as pd
import matplotlib.pyplot as plt

fig = plt.figure()

df = pd.read_csv('/Users/ericliao/Desktop/compare_similarity_score_between_original_and_new//Users/ericliao/Desktop/compare_similarity_score_between_original_and_new/high_resolution_peaks_table_test_10_percent.csv', header=0)

df_100 = df.loc[df['Counts'] <= 100]
# n, bins, patched = plt.hist(df_100['Count(*)'], bins=100, color='red', alpha=0.5)

n, bins, patched = plt.hist(df['Counts'], bins=200, color='red', alpha=0.5)

fig.suptitle('peak information', fontsize=10)

plt.yscale('log')
# plt.xscale('log')

plt.xlabel('number of peaks')
plt.ylabel('number of spectra')

plt.show()