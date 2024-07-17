import pandas as pd
from sklearn.preprocessing import StandardScaler
import operator
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

df_data = pd.read_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1066/RP/POS/aligned.csv"
)

df_factor = pd.read_csv(
    "/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1066/RP/POS/factors.csv"
)

df_height = df_data.loc[:, [" height" in i for i in df_data.columns]]
df_height = df_height.fillna(0)
df_height_transposed = df_height.T

# df_new = pd.DataFrame(columns=df_height_transposed.columns)
# df_new['target'] = ""
data_list = []

target = []

for index, row in df_height_transposed.iterrows():
    source_name = index.split(" ", 1)[0].strip()

    treatment_type = df_factor[df_factor["sample_files"] == source_name][
        "Factor Value[Health status]"
    ].values[0]

    if operator.contains(treatment_type, "Healthy"):
        target.append(0)
        row_dict = row.to_dict()
        row_dict["target"] = 0
        data_list.append(row_dict)

    if operator.contains(treatment_type, "breast cancer"):
        target.append(1)
        row_dict = row.to_dict()
        row_dict["target"] = 1
        data_list.append(row_dict)

    if operator.contains(treatment_type, "pool"):
        target.append(2)
        row_dict = row.to_dict()
        row_dict["target"] = 2
        data_list.append(row_dict)

    if operator.contains(treatment_type, "blank"):
        target.append(2)
        row_dict = row.to_dict()
        row_dict["target"] = 3
        data_list.append(row_dict)

df_new = pd.DataFrame.from_dict(data_list)

# data scaling
x_scaled = StandardScaler().fit_transform(df_height_transposed)

pca = PCA(n_components=2)

# Fit and transform data
pca_features = pca.fit_transform(x_scaled)

print(pca.explained_variance_)
print(pca.explained_variance_ratio_)

x_axis = "PC1 :" + "{:.2f}".format(pca.explained_variance_ratio_[0]) + "%"
y_axis = "PC2 :" + "{:.2f}".format(pca.explained_variance_ratio_[1]) + "%"


# Create dataframe
pca_df = pd.DataFrame(data=pca_features, columns=[x_axis, y_axis])

# map target names to PCA features
target_names = {0: "Health", 1: "Breast Cancer", 2: "Pool", 3: "Blank"}

pca_df["target"] = target
pca_df["target"] = pca_df["target"].map(target_names)

sns.set()

x_axis = "PC1 :" + "{:.2f}".format(pca.explained_variance_ratio_[0]) + "%"
y_axis = "PC2 :" + "{:.2f}".format(pca.explained_variance_ratio_[1]) + "%"

sns.lmplot(x=x_axis, y=y_axis, data=pca_df, hue="target", fit_reg=False, legend=True)

plt.title("MTBLS1066 RP Positive Mode PCA")
plt.show()
