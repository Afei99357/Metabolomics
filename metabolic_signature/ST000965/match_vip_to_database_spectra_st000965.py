import pandas as pd

df_database = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/studies"
                          "/ST000965/st000965_spectrum_infor.csv")

df_30 = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000965/results/0_min_vs_30_min.csv',
                      index_col=0)

df_60 = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000965/results/0_min_vs_60_min.csv',
                      index_col=0)

df_90 = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000965/results/0_min_vs_90_min.csv',
                      index_col=0)


df_90_new = df_90[['name', 'VIP']]

df_90_combine_database = pd.merge(df_database, df_90_new, how='outer', on="name", suffixes=('database', '_90'))

df_90_combine_database = df_90_combine_database.dropna()

df_output = df_90_combine_database[["SpectrumId", "VIP"]]

df_output = df_output.rename(columns={"SpectrumId": "SpectrumId", "VIP": "Score"})

columns = ["Comment", "PlsdaId"]

df_output = pd.concat([df_output, pd.DataFrame(columns=columns)])

df_output = df_output.assign(PlsdaId='18')
df_output = df_output.assign(Comment='0 min vs. 90 min')
df_output = df_output.reset_index(drop=True)

df_output.to_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/studies/ST000965/90_min_database_input.csv")

