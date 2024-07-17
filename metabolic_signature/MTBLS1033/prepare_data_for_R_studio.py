import pandas as pd
import operator

df = pd.read_csv("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/POS/"
                 "new_analysis/with_feature_selection/vips_annotated.csv")

df_factor = pd.read_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/NEG/MTBLS1033_factors.csv"
)

df_height = df.loc[:, [" height" in i for i in df.columns]]
df_height = df_height.fillna(0)
df_height_transposed = df_height.T

data_list = []
index_list = []
target = []

for index, row in df_height_transposed.iterrows():
    sample_name = index.split(" ", 1)[0]
    treatment_type = df_factor[df_factor["Source Name"] == sample_name][
        "Factor Value[Group]"
    ].values[0]
    if operator.contains(treatment_type, "Control"):
        row_dict = row.to_dict()
        data_list.append(row_dict)
        row_dict['target'] = 0
        index_list.append(sample_name)

    if operator.contains(treatment_type, "POP"):
        row_dict = row.to_dict()
        data_list.append(row_dict)
        row_dict['target'] = 1
        index_list.append(sample_name)

df_new = pd.DataFrame.from_dict(data_list).T

df_new.columns = index_list

df_new.to_csv("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/"
              "POS/new_analysis/R_STUDIO/r_input.csv")