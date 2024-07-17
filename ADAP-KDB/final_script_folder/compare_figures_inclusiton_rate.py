import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import string

# create 4 subplots
plt.figure().clear()
fig, axs = plt.subplots(2, 2, figsize=(6, 4))
fig.set_size_inches(11, 8)

df_low = pd.read_csv('/Users/ericliao/Desktop/manuscript_revise/Low_Intensity/inclusion_rate/inclusion_rate_low_res_new_method.csv', header=0, index_col=0)

df_1 = df_low.iloc[8:16, :]
df_2 = np.square(df_1)
ax_1 = sns.heatmap(df_2.T, linewidth=0.5, annot=df_1.T, annot_kws={"fontsize": 10}, fmt='.3f', cmap='Blues',
                   cbar=False, ax=axs[0, 0], vmin=0, vmax=1)

df_3 = df_low.iloc[0:8, :]
df_4 = np.square(df_3)
ax_2 = sns.heatmap(df_4.T, linewidth=0.5, annot=df_3.T, annot_kws={"fontsize": 10}, fmt='.3f', cmap='Blues',
                   cbar=False, ax=axs[0, 1], vmin=0, vmax=1)

df_high = pd.read_csv('/Users/ericliao/Desktop/manuscript_revise/High_Intensity/inclusion_rate/inclusion_rate_high_res_new_method.csv', header=0, index_col=0)

# df.style.background_gradient(cmap='viridis').set_properties(**{'font-size': '20px'})

df_5 = df_high.iloc[8:16, :]
df_6 = np.square(df_5)
ax_3 = sns.heatmap(df_6.T, linewidth=0.5, annot=df_5.T, annot_kws={"fontsize": 10}, fmt='.3f', cmap='Blues',
                   cbar=False, ax=axs[1, 0], vmin=0, vmax=1)

df_7 = df_high.iloc[0:8, :]
df_8 = np.square(df_7)
ax_4 = sns.heatmap(df_8.T, linewidth=0.5, annot=df_7.T, annot_kws={"fontsize": 10}, fmt='.3f', cmap='Blues',
                   cbar=False, ax=axs[1, 1], vmin=0, vmax=1)


label_font_size = 10
tick_font_size = 10

n = r"$\it{n}$"
m = r"$\it{m}$"
labels = [(n + '=4\n' + m + '=4'), (n + '=4\n' + m + '=7'), (n + '=6\n' + m + '=6'), (n + '=6\n' + m + '=11'),
          (n + '=8\n' + m + '=8'), (n + '=8\n' + m + '=15'), (n + '=12\n' + m + '=12'), (n + '=16\n' + m + '=16')]
r = r"$\it{R}$"

axs[0, 0].tick_params(axis='x', labelsize=label_font_size, rotation=0, length=0)
axs[0, 0].tick_params(axis='y', labelsize=label_font_size, length=0)
axs[0, 0].xaxis.label.set_size(label_font_size)
axs[0, 0].yaxis.label.set_size(label_font_size)
axs[0, 0].set_title('Inclusion Rate for Low-Res Spectra', fontsize='large')
for label in axs[0, 0].get_yticklabels():
    label.set_verticalalignment('center')
axs[0, 0].set_xlabel('Number of Compared Peaks', labelpad=6)
axs[0, 0].set_xticklabels(labels)

axs[0, 1].tick_params(axis='x', labelsize=label_font_size, length=0)
axs[0, 1].tick_params(axis='y', labelsize=label_font_size, length=0)
axs[0, 1].xaxis.label.set_size(label_font_size)
axs[0, 1].yaxis.label.set_size(label_font_size)
axs[0, 1].set_title('Inclusion Rate for Low-Res Spectra', fontsize='large')
for label in axs[0, 1].get_yticklabels():
    label.set_verticalalignment('center')
axs[0, 1].set_xlabel('Threshold ' + r, labelpad=7)

axs[1, 0].tick_params(axis='x', labelsize=label_font_size, rotation=0, length=0)
axs[1, 0].tick_params(axis='y', labelsize=label_font_size, length=0)
axs[1, 0].xaxis.label.set_size(label_font_size)
axs[1, 0].yaxis.label.set_size(label_font_size)
axs[1, 0].set_title('Inclusion Rate for High-Res Spectra', fontsize='large')
for label in axs[1, 0].get_yticklabels():
    label.set_verticalalignment('center')
axs[1, 0].set_xlabel('Number of Compared Peaks', labelpad=6)
axs[1, 0].set_xticklabels(labels)

axs[1, 1].tick_params(axis='x', labelsize=label_font_size, length=0)
axs[1, 1].tick_params(axis='y', labelsize=label_font_size, length=0)
axs[1, 1].xaxis.label.set_size(label_font_size)
axs[1, 1].yaxis.label.set_size(label_font_size)
axs[1, 1].set_title('Inclusion Rate for High-Res Spectra', fontsize='large')
for label in axs[1, 1].get_yticklabels():
    label.set_verticalalignment('center')
axs[1, 1].set_xlabel('Threshold ' + r, labelpad=7)

plt.text(0, 1.05, "(A)", size=12, transform=axs[0, 0].transAxes)
plt.text(0, 1.05, "(B)", size=12, transform=axs[0, 1].transAxes)
plt.text(0, 1.05, "(C)", size=12, transform=axs[1, 0].transAxes)
plt.text(0, 1.05, "(D)", size=12, transform=axs[1, 1].transAxes)

plt.subplots_adjust(left=0.8,
                    bottom=0.6,
                    right=0.9,
                    top=0.65,
                    wspace=0,
                    hspace=-0.999)
fig.tight_layout()


plt.savefig('/Users/ericliao/Desktop/manuscript_revise/figs/comparison_inclusion_rate_high_low.png', dpi=300)

# plt.show()