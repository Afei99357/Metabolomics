import pandas as pd
import matplotlib.pylab as plt
from matplotlib import gridspec
from sklearn.preprocessing import minmax_scale

fig, axes = plt.subplots(4, 1, sharex=True)

# set height ratios for subplots
gs = gridspec.GridSpec(4, 1)

mz_values = []
intensities = []
for line in open("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/adap_kdb_algorithm_comparison/"
                 "high_resolution_data/no_553_spectrum_mz_intensity.txt"):
    line = line.strip()
    mz, intensity = map(float, line.split(' ', 1))
    mz_values.append(mz)
    intensities.append(intensity)

new_dict = {'m/z': mz_values, 'intensities': minmax_scale(intensities)}
df = pd.DataFrame(new_dict)
ax_1 = plt.subplot(gs[0])
ax_1.bar(df['m/z'], df['intensities'])
ax_1.set_title('(A) Query Spectrum No.553', fontsize=10)
# ax_1.title.set_text('Query Spectrum No. 12', font=10)
ax_1.set_ylabel('Intensity')

df_new_2 = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/adap_kdb_algorithm_comparison/'
                       'high_resolution_data/spectrum_match_2152890_553.csv', header=0, index_col=0)

df_new_2 = df_new_2[['Mz', 'Intensity']]
ax_2 = plt.subplot(gs[1], sharex=ax_1)
ax_2.bar(df_new_2['Mz'], df_new_2['Intensity'])
ax_2.set_title('(B) Matched Library Spectrum No.2152890', fontsize=10)
# ax_2.title.set_text('Match Spectrum No.2152350', fontsize=10)
ax_2.set_ylabel('Intensity')

df_new = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/adap_kdb_algorithm_comparison/'
                     'high_resolution_data/spectrum_match_2152538_553.csv', header=0, index_col=0)
df_new = df_new[['Mz', 'Intensity']]
ax_3 = plt.subplot(gs[2], sharex=ax_2)
ax_3.bar(df_new['Mz'], df_new['Intensity'])
ax_3.set_title('(C) Matched Library Spectrum No.2152538', fontsize=10)
# ax_3.title.set_text('Match Spectrum No.2155637', fontsize=10)
ax_3.set_ylabel('Intensity')

df_new = pd.read_csv('/Users/ericliao/Desktop/spectrum_2152405.csv', header=0, index_col=0)
df_new = df_new[['Mz', 'Intensity']]
ax_4 = plt.subplot(gs[3], sharex=ax_3)
ax_4.bar(df_new['Mz'], df_new['Intensity'])
ax_4.set_title('(D) Matched Library Spectrum No.2152405', fontsize=10)
# ax_3.title.set_text('Match Spectrum No.2155637', fontsize=10)
ax_3.set_ylabel('Intensity')

plt.xlabel("m/z")
fig.tight_layout()
plt.savefig('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/'
            'adap_kdb_algorithm_comparison/high_resolution_data/spectrum_553_2152890_2152538_2152405.png', dpi=300)
