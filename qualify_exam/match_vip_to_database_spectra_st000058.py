import pandas as pd

df_database = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
                          "studies/ST000058/new_process/st000058_spectrum_infor.csv")

df_2hour = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000058/results/0_hour_vs_2_hours_st000058_vip_greater_0.csv',
                       index_col=0)

df_4hour = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000058/results/0_hour_vs_4_hours_st000058_vip_greater_0.csv',
                       index_col=0)

df_8hour = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000058/results/0_hour_vs_8_hours_st000058_vip_greater_0.csv',
                       index_col=0)

df_12hour = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000058/results/0_hour_vs_12_hours_st000058_vip_greater_0.csv',
                        index_col=0)

df_24hour = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000058/results/0_hour_vs_24_hours_st000058_vip_greater_0.csv',
                        index_col=0)

df_48hour = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000058/results/0_hour_vs_48_hours_st000058_vip_greater_0.csv',
                        index_col=0)


df_48hour_new = df_48hour[['name', 'VIP']]

df_48hour_combine_database = pd.merge(df_database, df_48hour_new, how='outer', on="name")

df_48hour_combine_database = df_48hour_combine_database.dropna()

df_output = df_48hour_combine_database[["SpectrumId", "VIP"]]

df_output = df_output.rename(columns={"SpectrumId": "SpectrumId", "VIP": "Score"})

columns = ["Comment", "PlsdaId"]

df_output = pd.concat([df_output, pd.DataFrame(columns=columns)])

df_output = df_output.assign(PlsdaId='6')
df_output = df_output.assign(Comment='48 hours vs. 0 hours')
df_output = df_output.reset_index(drop=True)

df_output.to_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/studies/ST000058/new_process/48hour_database_input.csv")


