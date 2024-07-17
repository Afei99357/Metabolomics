import pandas as pd


df = pd.read_csv("/Users/ericliao/Downloads/MTBLS27_compressed_files/"
                 "a_mtbls27_metabolite profiling_mass spectrometry.txt", sep="\t")

df_new = df.loc[:, ["Sample Name", "Raw Spectral Data File"]]

df_2 = pd.read_csv("/Volumes/MTBLS27/audit/20160204163430/s_MTBLS27.txt", sep="\t")

df_2_new = df_2.loc[:, [i for i in df_2.columns.tolist() if i.startswith("Factor Value") or i == "Sample Name"]]

df_merge = pd.merge(df_new, df_2_new, on="Sample Name")

df_merge.to_csv("/Users/ericliao/Desktop/MTBLS27_factors.csv")