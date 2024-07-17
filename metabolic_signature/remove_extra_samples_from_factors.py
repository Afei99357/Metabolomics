import glob
import pandas as pd
import os

df = pd.read_csv(r"C:\Users\yliao13\Desktop\New_folder\MTBLS196_neg.csv")
files = r"Z:\yliao13\new files\MTBLS196\samples\*"

file_name_list = glob.glob(files)

file_name_list = [os.path.basename(file) for file in file_name_list]

list_keep = [row['Sample Name'] in file_name_list for index, row in df.iterrows()]

df = df.loc[list_keep, :]

df.to_csv(r"C:\Users\yliao13\Desktop\New_folder\MTBLS196_neg_factors.csv")