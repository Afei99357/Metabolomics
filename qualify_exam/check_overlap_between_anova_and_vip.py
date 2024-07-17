import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import plot, UpSet

df = pd.read_csv('/Users/ericliao/Desktop/anova_vs_vip_results.csv', index_col=None,header=0)

fdr_5 = df['pvalue_fdr_5_percent'].unique().tolist()
fdr_10 = df['pvalue_fdr_10_percent'].unique().tolist()
vip_greater_1_3 = df['vip_greater_1.3'].unique().tolist()
vip_greater_1_5 = df['vip_greater_1.5'].unique().tolist()


all_metablites = set(fdr_5 + fdr_10 + vip_greater_1_3 + vip_greater_1_5)

# convert set to list for DataFrame index
labels = list(all_metablites)

## create a dataframe for plot upset plot
data = pd.DataFrame(index=labels, columns=['ANOVA FDR 5%', 'ANOVA FDR 10%',  "VIP > 1.3", "VIP > 1.5"])

# Fill the DataFrame: 1 if gene is in the list, 0 otherwise
data['ANOVA FDR 5%'] = data.index.isin(fdr_5).astype(int)
data['ANOVA FDR 10%'] = data.index.isin(fdr_10).astype(int)
data['VIP > 1.3'] = data.index.isin(vip_greater_1_3).astype(int)
data['VIP > 1.5'] = data.index.isin(vip_greater_1_5).astype(int)

# Convert DataFrame format for UpSetPlot
upset_data = data.groupby(list(data.columns)).size()

# Create the UpSet plot only with intersection of the data
plot(upset_data, orientation='horizontal', show_counts=True, sort_by='cardinality',
     show_percentages=True, element_size=50, )



# Save the plot
plt.savefig('/Users/ericliao/Desktop/anova_vs_vip_upset_plot.png', dpi=300)



