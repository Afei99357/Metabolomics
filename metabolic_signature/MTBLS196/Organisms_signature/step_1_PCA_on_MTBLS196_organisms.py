import pandas as pd
from sklearn.preprocessing import StandardScaler
import operator
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

df_data = pd.read_csv(
    "/Lab_work/data_files/metabolomics_signature/MTBLS196/Neg/aligned.csv"
)

df_factor = pd.read_csv(
    "/Lab_work/data_files/metabolomics_signature/MTBLS196/Neg/MTBLS196_neg_factors.csv"
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

    virus_type = df_factor[df_factor["Sample Name"] == source_name]["virus"].values[0]
    organism_part = df_factor[df_factor["Sample Name"] == source_name][
        "organism_part"
    ].values[0]
    time_collected = df_factor[df_factor["Sample Name"] == source_name][
        "time_collected"
    ].values[0]

    if operator.contains(virus_type, "1918") and operator.contains(
        organism_part, "lung"
    ):
        target.append(0)
        row_dict = row.to_dict()
        row_dict["target"] = 0
        data_list.append(row_dict)

    if operator.contains(virus_type, "Cal04RG") and operator.contains(
        organism_part, "lung"
    ):
        target.append(1)
        row_dict = row.to_dict()
        row_dict["target"] = 1
        data_list.append(row_dict)

    if operator.contains(virus_type, "mock") and operator.contains(
        organism_part, "lung"
    ):
        target.append(2)
        row_dict = row.to_dict()
        row_dict["target"] = 2
        data_list.append(row_dict)

    if operator.contains(virus_type, "1918") and operator.contains(
        organism_part, "trachea"
    ):
        target.append(3)
        row_dict = row.to_dict()
        row_dict["target"] = 3
        data_list.append(row_dict)

    if operator.contains(virus_type, "Cal04RG") and operator.contains(
        organism_part, "trachea"
    ):
        target.append(4)
        row_dict = row.to_dict()
        row_dict["target"] = 4
        data_list.append(row_dict)

    if operator.contains(virus_type, "mock") and operator.contains(
        organism_part, "trachea"
    ):
        target.append(5)
        row_dict = row.to_dict()
        row_dict["target"] = 5
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
target_names = {
    0: "1918_lung",
    1: "Cal04RG_lung",
    2: "mock_lung",
    3: "1918_trachea",
    4: "Cal04RG_trachea",
    5: "mock_trachea",
}

pca_df["target"] = target
pca_df["target"] = pca_df["target"].map(target_names)

sns.set()

x_axis = "PC1 :" + "{:.2f}".format(pca.explained_variance_ratio_[0]) + "%"
y_axis = "PC2 :" + "{:.2f}".format(pca.explained_variance_ratio_[1]) + "%"

sns.lmplot(x=x_axis, y=y_axis, data=pca_df, hue="target", fit_reg=False, legend=True)

plt.title("MTBLS196 negative mode PCA")
plt.show()
