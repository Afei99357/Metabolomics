import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import string

# create 4 subplots
plt.figure().clear()
fig, axs = plt.subplots(2, 2, figsize=(6, 4))
# fig.set_size_inches(11, 8)


df_inclusion_rate = pd.read_csv('/Users/ericliao/Desktop/manuscript_revise/Low_Intensity/inclusion_rate_low_res.csv', header=0, index_col=0)

# df.style.background_gradient(cmap='viridis').set_properties(**{'font-size': '20px'})

df_1 = df_inclusion_rate.iloc[8:16, :]
df_2 = np.square(df_1)
ax_1 = sns.heatmap(df_2.T, linewidth=0.5, annot=df_1.T, annot_kws={"fontsize": 5}, fmt='.3f', cmap='Blues',
                   cbar=False, ax=axs[0, 1], vmin=0, vmax=1)

df_3 = df_inclusion_rate.iloc[0:8, :]
df_4 = np.square(df_3)
ax_2 = sns.heatmap(df_4.T, linewidth=0.5, annot=df_3.T, annot_kws={"fontsize": 5}, fmt='.3f', cmap='Blues',
                   cbar=False, ax=axs[1, 1], vmin=0, vmax=1)

# df2 = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/adap_kdb_algorithm_comparison/"
#                   "time_cost.csv", header=0, index_col=0)
#
# df3 = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/adap_kdb_algorithm_comparison/"
#                   "time_cost_for_histogram.csv", header=0, index_col=0)

# axs[0, 0].plot(df3.index.values, df3['Average'].values)

# ############# plot for threshold 50 with different prescreen parameter
# x_axis = ['4 peaks', '6 peaks', '8 peaks', '12 peaks', '16 peaks']
#
# time_seris = df3[['Average']]
#
# y_axis = np.zeros((5, 2))
#
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
# df_histogram.plot.bar(ax=axs[0, 0])
#
# axs[0, 0].tick_params(labelrotation=0)
#
# labels = ['Approach 1', 'Approach 2']
# axs[0, 0].legend(labels=labels, loc='upper right')
# ##################################################

df_8_15 = pd.read_csv('/Users/ericliao/Desktop/manuscript_revise/Low_Intensity/time_cost/different_threshold_8_15_time_cost_combine_low_res.csv',
                      header=0, index_col=0)

(df_8_15 / 1000).boxplot(ax=axs[1, 0], sym='', showmeans=True, meanprops={"marker": "o",
                                                                          "markerfacecolor": "white",
                                                                          "markeredgecolor": "black",
                                                                          "markersize": "2"})

df_threshold_50 = pd.read_csv(
    '/Users/ericliao/Desktop/manuscript_revise/Low_Intensity/time_cost/threshold_50_different_parameter_time_cost_combine_low_res.csv',
    header=0, index_col=0)

(df_threshold_50 / 1000).boxplot(ax=axs[0, 0], sym='', showmeans=True, meanprops={"marker": "o",
                                                                                  "markerfacecolor": "white",
                                                                                  "markeredgecolor": "black",
                                                                                  "markersize": "2"})

# groups = df3.groupby('group')
#
# for group in groups:
#     plt.bar(group['Pre-screen Parameter'], group['Average'], label=group['Pre-screen Parameter'], align='center')
#

# axs[1, 0].bar(list(df2.index.values[8:16]), list(df2['Average'][8:16].values))
# axs[0, 0].barh(list(df3.index.values[8:16]), list(df3['Average'][8:16].values))

label_font_size = 6
tick_font_size = 6

# ax.tick_params(axis='x', rotation=90, labelsize=50)
axs[0, 0].tick_params(axis='x', labelsize=label_font_size, length=2)
axs[0, 0].tick_params(axis='y', labelsize=label_font_size, length=2)
axs[0, 0].xaxis.label.set_size(label_font_size)
axs[0, 0].yaxis.label.set_size(label_font_size)
axs[0, 0].set_xlabel('Number of Compared Peaks', labelpad=6)
axs[0, 0].set_ylabel('Execution Time, sec', labelpad=6)
n = r"$\it{n}$"
m = r"$\it{m}$"
labels = [(n + '=4\n' + m + '=4'), (n + '=4\n' + m + '=7'), (n + '=6\n' + m + '=6'), (n + '=6\n' + m + '=11'),
          (n + '=8\n' + m + '=8'), (n + '=8\n' + m + '=15'), (n + '=12\n' + m + '=12'), (n + '=16\n' + m + '=16')]
axs[0, 0].set_xticklabels(labels)


axs[1, 0].tick_params(axis='x', labelsize=label_font_size, length=2)
axs[1, 0].tick_params(axis='y', labelsize=label_font_size, length=2)
axs[1, 0].xaxis.label.set_size(label_font_size)
axs[1, 0].yaxis.label.set_size(label_font_size)
r = r"$\it{R}$"
axs[1, 0].set_xlabel('Threshold ' + r, labelpad=6)
axs[1, 0].set_ylabel('Execution Time, sec', labelpad=6)


axs[0, 1].tick_params(axis='x', labelsize=label_font_size, rotation=0, length=0)
axs[0, 1].tick_params(axis='y', labelsize=label_font_size, length=0)
axs[0, 1].xaxis.label.set_size(label_font_size)
axs[0, 1].yaxis.label.set_size(label_font_size)
axs[0, 1].set_title('Inclusion Rate', fontsize='small')
for label in axs[0, 1].get_yticklabels():
    label.set_verticalalignment('center')
axs[0, 1].set_xlabel('Number of Compared Peaks', labelpad=6)
axs[0, 1].set_xticklabels(labels)

axs[1, 1].tick_params(axis='x', labelsize=label_font_size, length=0)
axs[1, 1].tick_params(axis='y', labelsize=label_font_size, length=0)
axs[1, 1].xaxis.label.set_size(label_font_size)
axs[1, 1].yaxis.label.set_size(label_font_size)
axs[1, 1].set_title('Inclusion Rate', fontsize='small')
for label in axs[1, 1].get_yticklabels():
    label.set_verticalalignment('center')
axs[1, 1].set_xlabel('Threshold ' + r, labelpad=7)

plt.text(-0.1, 1.05, "(A)", size=8, transform=axs[0, 0].transAxes)
plt.text(0.1, 1.05, "Original Time: 12.522 seconds/spectrum", size=5, transform=axs[0, 0].transAxes, c="red")

plt.text(-0.1, 1.05, "(B)", size=8, transform=axs[0, 1].transAxes)

plt.text(-0.1, 1.05, "(C)", size=8, transform=axs[1, 0].transAxes)
plt.text(0.1, 1.05, "Original Time: 12.522 seconds/spectrum", size=5, transform=axs[1, 0].transAxes, c="red")

plt.text(-0.1, 1.05, "(D)", size=8, transform=axs[1, 1].transAxes)

plt.subplots_adjust(left=0.8,
                    bottom=0.6,
                    right=0.9,
                    top=0.65,
                    wspace=0,
                    hspace=-0.999)
fig.tight_layout()

plt.savefig('/Users/ericliao/Desktop/manuscript_revise/Low_Intensity/plots/comparison_low_res.png', dpi=300)

# plt.show()