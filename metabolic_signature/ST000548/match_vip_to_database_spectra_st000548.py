import pandas as pd

df_database = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/studies"
                          "/ST000964/st000964_spectrum_infor.csv")

df_old_young = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000964/results/old_vs_young_st000964_vip_greater_0.csv',
                      index_col=0)

df_different_treatment = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000964/results/2.8mM_vs_16.8mM_st000964_vip_greater_0.csv',
                      index_col=0)

df_old_young_168 = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000964/results/old_16.8mM_vs_young_16.8mM_st000964_vip_greater_0.csv',
                      index_col=0)

df_old_young_28 = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000964/results/old_2.8mM_vs_young_2.8mM_st000964_vip_greater_0.csv',
                      index_col=0)


df_old_young_28_new = df_old_young[['name', 'VIP']]

df_old_young_28_combine_database = pd.merge(df_database, df_old_young_28_new, how='outer', on="name", suffixes=('database', '_old_young_28'))

df_Bold_young_combine_database = df_old_young_28_combine_database.dropna()

df_output = df_old_young_28_combine_database[["SpectrumId", "VIP"]]

df_output = df_output.rename(columns={"SpectrumId": "SpectrumId", "VIP": "Score"})

columns = ["Comment", "PlsdaId"]

df_output = pd.concat([df_output, pd.DataFrame(columns=columns)])

df_output = df_output.assign(PlsdaId='15')
df_output = df_output.assign(Comment='Old 2.8Mm vs. Young 2.8Mm')
df_output = df_output.reset_index(drop=True)

df_output.to_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/studies/ST000964/old_young_28_database_input.csv")

