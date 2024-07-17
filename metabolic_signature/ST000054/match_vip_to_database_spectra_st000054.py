import pandas as pd

df_database = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/studies"
                          "/ST000054/st000054_spectrum_infor.csv")

df_LumA = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000054/results/LumA_vs_Non_LumA_st000054_vips_greater_0.csv',
                      index_col=0)

df_LumB = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000054/results/LumB_vs_Non_LumB_st000054_vips_greater_0.csv',
                      index_col=0)

df_HER2 = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000054/results/HER2_vs_Non_HER2_st000054_vips_greater_0.csv',
                      index_col=0)

df_DCIS = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000054/results/DCIS_vs_Non_DCIS_st000054_vips_greater_0.csv',
                      index_col=0)

df_Basal = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000054/results/Basal_vs_Non_Basal_st000054_vips_greater_0.csv',
                       index_col=0)


df_Basal_new = df_LumA[['name', 'VIP']]

df_Basal_combine_database = pd.merge(df_database, df_Basal_new, how='outer', on="name", suffixes=('database', '_Basal'))

df_Basal_combine_database = df_Basal_combine_database.dropna()

df_output = df_Basal_combine_database[["SpectrumId", "VIP"]]

df_output = df_output.rename(columns={"SpectrumId": "SpectrumId", "VIP": "Score"})

columns = ["Comment", "PlsdaId"]

df_output = pd.concat([df_output, pd.DataFrame(columns=columns)])

df_output = df_output.assign(PlsdaId='10')
df_output = df_output.assign(Comment='Reduction vs. Basal')
df_output = df_output.reset_index(drop=True)

df_output.to_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/studies/ST000054/Basal_database_input.csv")


