import pandas as pd
import matplotlib.pylab as plt
from sklearn.preprocessing import minmax_scale


mz_values = []
intensities = []
for line in open("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/adap_kdb_algorithm_comparison/"
                 "high_resolution_data/no_553_spectrum_mz_intensity.txt"):
    line = line.strip()
    mz, intensity = map(float, line.split(' ', 1))
    mz_values.append(mz)
    intensities.append(-intensity)

new_dict = {'m/z': mz_values, 'intensities': -minmax_scale(intensities)}


def autolabel(mzs, intensities):
    """
    Attach a text label above each bar displaying its height
    """
    for mz_value, intensity_value in zip(mzs, intensities):
        plt.annotate('{:.4f}'.format(mz_value), xy=(mz_value, intensity_value), xytext=(0, 5), textcoords='offset points', ha='center')
        # ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
        #         "{:.4f}".format(mz),
        #         ha='center', va='bottom')

for i in range(40, 270, 10):
    df = pd.DataFrame(new_dict)

    df_new_2 = pd.read_csv(
        '/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/adap_kdb_algorithm_comparison/'
        'high_resolution_data/spectrum_match_2152538_553.csv', header=0, index_col=0)
    fig, ax = plt.subplots()
    begin = i
    end = i+10

    df = df[df['m/z'].between(begin, end, inclusive=False)]
    stems_1 = plt.stem(df['m/z'], df['intensities'], 'b', label='query spectrum', linefmt='C0', markerfmt=' ')
    # rects1 = plt.bar(df['m/z'], df['intensities'], width=0.01)

    df_new_2 = df_new_2[df_new_2['Mz'].between(begin, end, inclusive=False)]
    df_new_2 = df_new_2[['Mz', 'Intensity']]
    stems_2 = plt.stem(df_new_2['Mz'], df_new_2['Intensity']*75, 'g', label='library spectrum', linefmt='C1', markerfmt=' ')

    # rects2 = plt.bar(df_new_2['Mz'], df_new_2['Intensity']*20, width=0.01)

    autolabel(df['m/z'], df['intensities'])
    autolabel(df_new_2['Mz'], df_new_2['Intensity'])

    plt.xlabel("m/z")
    plt.legend()
    fig.tight_layout()
    plt.savefig('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/'
                'adap_kdb_algorithm_comparison/high_resolution_data/temp/spectrum_553_2152358_partial_' + str(begin) +
                '_and_' + str(end) + '_check.png', dpi=300)
    plt.close(fig)
