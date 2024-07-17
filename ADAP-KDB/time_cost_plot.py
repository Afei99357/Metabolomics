import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df3 = pd.read_csv("/Users/yliao13/phd_class_code/Lab_work/data_files/"
                 "adap_kdb_algorithm_comparison/time_cost.csv", header=0, index_col=0)

############ plot for different threshold parameters
fig, ax = plt.subplots(figsize=(30, 40))
# ax.plot(df.index.values, df['Average'].values)
# ax.bar(list(df.index.values[0:8]), list(df['Average'][0:8].values))
# ax.bar(list(df.index.values[8:16]), list(df['Average'][8:16].values))
ax.barh(list(df3.index.values[8:16]), list(df3['Average'][8:16].values))

# ax.tick_params(axis='x', rotation=90, labelsize=50)
ax.tick_params(axis='x', labelsize=50)
ax.tick_params(axis='y', labelsize=50)

ax.xaxis.label.set_size(50)
ax.yaxis.label.set_size(50)

# axs[0].yaxis.set_ticks(np.arange(0, 6, 0.5))

ax.set_ylabel('Different Spectra Return Threshold')
ax.set_xlabel('Average Time Cost (Seconds)')

############## plot for threshold 50 with different prescreen parameter
# x_axis = ['4 peaks', '6 peaks', '8 peaks', '12 peaks', '16 peaks']

# time_seris = df[['Average']]

# y_axis = np.zeros((5, 2))

# n = 0
# for cell in y_axis:
#     if len(time_seris) == n:
#         break
#     cell[0] = time_seris.values[n]
#     cell[1] = time_seris.values[n+1]
#     n = n + 2
#
# print(y_axis)
# df_histogram = pd.DataFrame(y_axis, index=x_axis)
# df_histogram.plot.bar()

# plt.tick_params(axis='x', rotation=0)
# plt.ylabel('time cost (seconds)')
#
# labels = ['Approach 1', 'Approach 2']
# plt.legend(labels=labels, loc='upper right')

plt.subplots_adjust(bottom=0.1)
plt.show()
