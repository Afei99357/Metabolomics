import os
import pandas as pd
input_directory = "/Users/yliao13/Desktop/ST000058SAMPLES/"

df = pd.read_csv("/Users/yliao13/Desktop/factors.csv")

id_list = []
file_list = []

for i in df["local_sample_id"].tolist():
    id_list.append(i.strip())


for root, subdirectories, files in os.walk(input_directory):
    for file in files:
        file_id = file.split(".", 2)[0]
        file_list.append(file_id)
        if file_id not in id_list:
            print("missing from files: " + file)


for i in id_list:
    if i not in file_list:
        print("missing from factor file: " + i)

