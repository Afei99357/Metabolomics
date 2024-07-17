import pandas as pd

df = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/adap_kdb_algorithm_comparison/"
                 "high_resolution_spectra_informtion/all_library_spectrum_information_high_resolution.csv", header=0)

df_new = df.loc[:, 'TopMz1':'TopMz16']

spectra_list = []

for index, row in df_new.iterrows():
    i = 0
    mz_ordered = row.sort_values()
    for n in range(len(row)):
        if (i + 1) > len(row):
            break
        if abs(mz_ordered[i] - mz_ordered[i + 1]) < 0.2:
            spectra_list.append(df['Id'][index])
        i += i

print(set(spectra_list))
print(len(set(spectra_list)))

df.loc[df['Id'].isin(set(spectra_list))] \
    .to_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/adap_kdb_algorithm_comparison/'
            'high_resolution_spectra_informtion/library_spectra_with_close_top_mz_0.2.csv')

