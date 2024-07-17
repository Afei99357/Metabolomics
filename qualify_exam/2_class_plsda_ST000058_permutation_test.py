import pandas as pd
import numpy as np
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2
import random
from matplotlib import pyplot as plt

### modify 1
df_new = pd.read_csv('/Users/ericliao/Downloads/st000058_group7.csv', index_col=0)

sample_size = 8

q2_list = []

for i in range(10000):
    target = [random.randint(0, 1) for _ in range(sample_size)]

    target = np.array(target)

    plsr = pls_da_model.pls_da(df_new, target, 0)

    # ########## calculate VIPs vector ######################
    # vip_value = vips.vips(plsr)
    #
    # vip_index = np.argsort(vip_value)

    ######### print out the q2 with leave one out cross-validation #####
    q2 = calculate_q2.calculate_q2(df_new, target, 2, 0)
    ####################################################################

    q2_list.append(q2[0])
    print(i)

q2_results = pd.Series(q2_list)

fig, ax = plt.subplots(figsize=(6, 4))
plt.style.use('bmh')

# Plot histogram
q2_results.plot(kind="hist", density=True, alpha=0.65,  bins=25)
# Plot KDE
q2_results.plot(kind="kde")

ax.set_xlabel("Q2 value")
ax.set_xlim(-3, 1.5)
# ax.set_xticks()

ax.set_ylim(0, 1)

ax.set_yticks([])
ax.set_ylabel('Frequency')

ax.grid(False)

# Quantile lines
quant_5, quant_25, quant_50, quant_75, quant_95 = q2_results.quantile(0.05), q2_results.quantile(0.25), q2_results.quantile(0.5), q2_results.quantile(0.75), q2_results.quantile(0.95)

quants = [[quant_5, 0.6, 0.16], [quant_25, 0.8, 0.26], [quant_50, 1, 0.36],  [quant_75, 0.8, 0.46], [quant_95, 0.6, 0.56]]
for i in quants:
    ax.axvline(i[0], alpha=i[1], ymax=i[2], linestyle=":")

# Annotations
ax.text(quant_5-.1, 0.17, "5th", size = 12, alpha = 0.8)
ax.text(quant_25-.13, 0.27, "25th", size = 11, alpha = 0.85)
ax.text(quant_50-.13, 0.37, "50th", size = 12, alpha = 1)
ax.text(quant_75-.13, 0.47, "75th", size = 11, alpha = 0.85)
ax.text(quant_95-.25, 0.57, "95th Percentile", size = 12, alpha =.8)

ax.tick_params(left=False, bottom=False)
for ax, spine in ax.spines.items():
    spine.set_visible(False)

plt.show()

