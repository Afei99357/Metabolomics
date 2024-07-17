import pandas as pd
import matplotlib.pylab as plt
import numpy as np

df = pd.read_csv('/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/adap_kdb_algorithm_comparison/'
                 'adap_kdb_high_res_similarity_score_result_with_different_tolerance/'
                 'fowlkes_mallows_score_with_different_threshold.csv')

df

plt.plot(df['threshold'], df['score'])

plt.xlabel("Threshold")
plt.ylabel("Fowlkes Mallows Score")
plt.xticks(np.arange(0, 1.1, step=0.1))

plt.show()