import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
from matplotlib.lines import Line2D
import matplotlib
import numpy as np
import string


# create 4 subplots
plt.figure().clear()
fig, axs = plt.subplots(2, 2, figsize=(6, 4))
# fig.set_size_inches(11, 8)

df_time_8_15_low = pd.read_csv('/Users/ericliao/Desktop/manuscript_revise/Low_Intensity/time_cost/different_threshold_8_15_time_cost_combine_low_res.csv',
                               header=0, index_col=0)

(df_time_8_15_low / 1000).boxplot(ax=axs[0, 1], sym='', showmeans=True, meanprops={"marker": "o",
                                                                          "markerfacecolor": "white",
                                                                          "markeredgecolor": "black",
                                                                          "markersize": "2"})

df_threshold_50_time_low = pd.read_csv(
    '/Users/ericliao/Desktop/manuscript_revise/Low_Intensity/time_cost/threshold_50_different_parameter_time_cost_combine_low_res.csv', header=0, index_col=0)

(df_threshold_50_time_low / 1000).boxplot(ax=axs[0, 0], sym='', showmeans=True, meanprops={"marker": "o",
                                                                                           "markerfacecolor": "white",
                                                                                           "markeredgecolor": "black",
                                                                                           "markersize": "2"})

df_time_8_15_high = pd.read_csv('/Users/ericliao/Desktop/manuscript_revise/High_Intensity/time_cost/different_threshold_8_15_time_cost_combine_high_res.csv', header=0, index_col=0)

(df_time_8_15_high / 1000).boxplot(ax=axs[1, 1], sym='', showmeans=True, meanprops={"marker": "o",
                                                                                    "markerfacecolor": "white",
                                                                                    "markeredgecolor": "black",
                                                                                    "markersize": "2"})

df_threshold_50_time_high = pd.read_csv(
    '/Users/ericliao/Desktop/manuscript_revise/High_Intensity/time_cost/threshold_50_different_parameter_time_cost_combine_high_res.csv', header=0, index_col=0)

(df_threshold_50_time_high / 1000).boxplot(ax=axs[1, 0], sym='', showmeans=True, meanprops={"marker": "o",
                                                                                            "markerfacecolor": "white",
                                                                                            "markeredgecolor": "black",
                                                                                            "markersize": "2"})

label_font_size = 6
tick_font_size = 5

n = r"$\it{n}$"
m = r"$\it{m}$"
r = r"$\it{R}$"
labels = [(n + '=4\n' + m + '=4'), (n + '=4\n' + m + '=7'), (n + '=6\n' + m + '=6'), (n + '=6\n' + m + '=11'),
          (n + '=8\n' + m + '=8'), (n + '=8\n' + m + '=15'), (n + '=12\n' + m + '=12'), (n + '=16\n' + m + '=16')]

# ax.tick_params(axis='x', rotation=90, labelsize=50)
axs[0, 0].tick_params(axis='x', labelsize=label_font_size, length=2)
axs[0, 0].tick_params(axis='y', labelsize=label_font_size, length=2)
axs[0, 0].xaxis.label.set_size(label_font_size)
axs[0, 0].yaxis.label.set_size(label_font_size)
# axs[0, 0].set_title("Low-Res Spectra \n" + r"$\bf{" + "\ (Original\ Time:\ 12.522\ seconds/spectrum)" + "}$", fontsize='x-small')
axs[0, 0].set_title("Low-Res Spectra", fontsize='x-small')
axs[0, 0].set_xlabel('Number of Compared Peaks', labelpad=6)
axs[0, 0].set_ylabel('Execution Time, sec', labelpad=6)
axs[0, 0].set_xticklabels(labels)
axs[0, 0].set_ylim([0, 13])

axs[0, 0].axhline(y=12.522, color='r', linestyle='-', lw=1)
lines = [Line2D([2, 8], [12.522, 12.522], c="red", lw=1.0)]
axs[0, 0].legend(lines, ['Original search time'], loc=7, bbox_to_anchor=(1, 0.85), fontsize=4, shadow=None)


axs[0, 1].tick_params(axis='x', labelsize=label_font_size, length=2)
axs[0, 1].tick_params(axis='y', labelsize=label_font_size, length=2)
axs[0, 1].xaxis.label.set_size(label_font_size)
axs[0, 1].yaxis.label.set_size(label_font_size)
# axs[0, 1].set_title("Low-Res Spectra \n" + r"$\bf{" + "\ (Original\ Time:\ 12.522\ seconds/spectrum)" + "}$", fontsize='x-small')
axs[0, 1].set_title("Low-Res Spectra", fontsize='x-small')
axs[0, 1].set_xlabel('Threshold ' + r, labelpad=6)
axs[0, 1].set_ylabel('Execution Time, sec', labelpad=6)
axs[0, 1].set_ylim([0, 13])

axs[0, 1].axhline(y=12.522, color='r', linestyle='-', lw=1)
axs[0, 1].legend(lines, ['Original search time'], loc=7, bbox_to_anchor=(1, 0.85), fontsize=4, shadow=None)

# plt.text(0.1, 1.15, "Original Time: 12.522", size=5, transform=axs[0, 1].transAxes, c="red")


# ax.tick_params(axis='x', rotation=90, labelsize=50)
axs[1, 0].tick_params(axis='x', labelsize=label_font_size, length=2)
axs[1, 0].tick_params(axis='y', labelsize=label_font_size, length=2)
axs[1, 0].xaxis.label.set_size(label_font_size)
axs[1, 0].yaxis.label.set_size(label_font_size)
# axs[1, 0].set_title("High-Res Spectra \n" + r"$\bf{" + "\ (Original\ Time:\ 3.399\ seconds/spectrum)" + "}$", fontsize='x-small')
axs[1, 0].set_title("High-Res Spectra", fontsize='x-small')
axs[1, 0].set_xlabel('Number of Compared Peaks', labelpad=6)
axs[1, 0].set_ylabel('Execution Time, sec', labelpad=6)
axs[1, 0].set_xticklabels(labels)
axs[1, 0].set_ylim([0, 7])

axs[1, 0].axhline(y=3.399, color='r', linestyle='-', lw=1)
lines = [Line2D([2, 8], [3.399, 3.399], c="red", lw=1.0)]
axs[1, 0].legend(lines, ['Original search time'], loc=1, fontsize=4, shadow=None)
# plt.text(0.1, 1.15, "Original Time: 3.115", size=5, transform=axs[1, 0].transAxes, c="red")


axs[1, 1].tick_params(axis='x', labelsize=label_font_size, length=2)
axs[1, 1].tick_params(axis='y', labelsize=label_font_size, length=2)
axs[1, 1].xaxis.label.set_size(label_font_size)
axs[1, 1].yaxis.label.set_size(label_font_size)
# axs[1, 1].set_title("High-Res Spectra \n" + r"$\bf{" + "\ (Original\ Time:\ 3.399\ seconds/spectrum)" + "}$", fontsize='x-small')
axs[1, 1].set_title("High-Res Spectra", fontsize='x-small')
axs[1, 1].set_xlabel('Threshold ' + r, labelpad=6)
axs[1, 1].set_ylabel('Execution Time, sec', labelpad=6)
axs[1, 1].set_ylim([0, 13])

axs[1, 1].axhline(y=3.399, color='r', linestyle='-', lw=1)
axs[1, 1].legend(lines, ['Original search time'], loc=1, fontsize=4, shadow=None)
# plt.text(0.1, 1.15, "Original Time: 3.115", size=5, transform=axs[1, 1].transAxes, c="red")


plt.text(-0.1, 1.1, "(A)", size=8, transform=axs[0, 0].transAxes)
plt.text(-0.1, 1.1, "(B)", size=8, transform=axs[0, 1].transAxes)
plt.text(-0.1, 1.1, "(C)", size=8, transform=axs[1, 0].transAxes)
plt.text(-0.1, 1.1, "(D)", size=8, transform=axs[1, 1].transAxes)

plt.subplots_adjust(left=0.8,
                    bottom=0.6,
                    right=0.9,
                    top=0.65,
                    wspace=0,
                    hspace=-0.999)
fig.tight_layout()

plt.savefig('/Users/ericliao/Desktop/manuscript_revise/figs/comparison_time_high_low_new.png', dpi=300)

# plt.show()