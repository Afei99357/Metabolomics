from sklearn.cluster import AgglomerativeClustering
import pandas as pd
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('/Users/ericliao/Desktop/TEMP_TEST/ST000054/aligned.csv')

df_height = df.loc[:, [' height' in i for i in df.columns]]

df_height = df_height.fillna(0)

df_height_transposed = df_height.T

model = AgglomerativeClustering(n_clusters=2, linkage='ward', compute_distances=True, affinity='euclidean')
# model = AgglomerativeClustering(n_clusters=2, linkage='average', compute_distances=True, affinity='euclidean')
model = model.fit(df_height_transposed)


def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)



plt.title('Hierarchical Clustering Dendrogram')
plot_dendrogram(model, truncate_mode=None)
plt.xlabel("Number of points in node.")

print(plt.xticks()[1])

plt.savefig('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/studies/ST000054'
            '/ward_linkage_euclidean_distance_dendrogram.png', dpi=300)

# plt.show()

