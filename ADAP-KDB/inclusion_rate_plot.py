import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("/Users/yliao13/phd_class_code/Lab_work/data_files/adap_kdb_algorithm_comparison/inclusion_rate_1110.csv",
                 header=0, index_col=0)
df = df.T

fig, ax = plt.subplots(figsize=(10, 10))

# df_diff_threshold = df.T.iloc[8:16, :]

# df_diff_threshold.plot.bar(stacked=True)
plt.xlabel('Different Prescreening parameters(peaks in query spectrum _ peaks in library spectrum)')
plt.legend(loc='upper right')

# for index, row in df.iterrows():
#     ax.plot(df.columns.values[0:8], row.values[0:8])
#     # ax.plot(df.columns.values[8:16], row.values[8:16])

df_histogram = pd.DataFrame(df.T.iloc[0:8, :], index=df.columns.values[0:8])
df_histogram.plot.bar(width=0.8)

ax.legend(df.index.values, loc="upper right")

ax.tick_params(axis='x', rotation=90, labelsize=10)
ax.tick_params(axis='y', labelsize=10)

ax.xaxis.label.set_size(10)
ax.yaxis.label.set_size(10)

# ax.xaxis.set_ticklabels(x_axis_labels)
# ax.set_xlabel('Different Prescreen Parameter (Peaks in query spectrum _ peaks in library spectrum)')
ax.set_xlabel('Different Spectra Return Threshold')
ax.set_ylabel('Inclusion Rate')

plt.subplots_adjust(bottom=0.19)
plt.show()