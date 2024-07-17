import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
import numpy as np

df = pd.read_csv('/Lab_work/data_files/adap_kdb_algorithm_comparison/inclusion_rate_1110.csv', header=0, index_col=0)

# df.style.background_gradient(cmap='viridis').set_properties(**{'font-size': '20px'})

df_1 = df.iloc[8:16, :]

df_2 = np.square(df_1)

ax = sns.heatmap(df_2, linewidth=0.5, annot=df_1, fmt='.3f', cmap='Greens')
plt.show()

