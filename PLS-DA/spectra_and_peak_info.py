import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/ericliao/Desktop/compare_similarity_score_between_original_and_new/high_resolution_peaks_table_test.csv', header=0)

specta_unique_list = df.SpectrumId.unique()

above_threshold_dict = {}

for i in specta_unique_list:
    df_current_spectrum = df.loc[df['SpectrumId'] == i]
    max_value = df_current_spectrum['Intensity'].max()
    threshold_1_percent = max_value * 0.1
    df_above_threshold = df_current_spectrum.loc[df_current_spectrum['Intensity'] >= threshold_1_percent]
    number_of_peaks = df_above_threshold.index.size
    above_threshold_dict.update({i: number_of_peaks})


df_final = pd.DataFrame(list(above_threshold_dict.items()), columns=['Spectrum ID', 'Counts'])

fig = plt.figure(1)

# df_final.to_csv('/Users/ericliao/Desktop/compare_similarity_score_between_original_and_new/low_resolution_spectra_peaks_info_no_filter_0_100.csv')
# n, bins, patched = plt.hist(df_final['Counts'], bins=200, color='red', alpha=0.5)


df_100 = df_final.loc[df_final['Counts'] <= 100]
n, bins, patched = plt.hist(df_100['Counts'], bins=100, color='red', alpha=0.5)

fig.suptitle('peak information', fontsize=10)

plt.yscale('log')

plt.xlabel('number of peaks')
plt.ylabel('number of spectra')

plt.show()