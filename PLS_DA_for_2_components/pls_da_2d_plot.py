# Author: Eric Liao
# August 2021

import matplotlib.pyplot as plt
import pandas as pd


class plot_2d:
    def plsda_2d_plot(
        scores,
        target_color,
        target_names,
        target_number,
        title_name=None,
        sample_labels_list=None,
    ):
        #### 2D plot for PLS-DA #######
        plt.style.use("ggplot")
        plot = plt.scatter(
            scores[:, 0],
            scores[:, 1],
            c=target_color,
            edgecolors="none",
            alpha=0.7,
            cmap=plt.cm.get_cmap("Set1", target_number),
            s=70,
        )
        plt.xlabel("Scores on LV 1")
        plt.ylabel("Scores on LV 2")
        classes = target_names.tolist()
        plt.legend(handles=plot.legend_elements()[0], labels=classes)

        ### add function to label each sample on pls-da plot
        if sample_labels_list is not None:
            scores_df = pd.DataFrame(scores)
            scores_df.index = sample_labels_list
            for n, (x, y) in enumerate(scores_df.values):
                label = scores_df.index.values[n]
                plt.text(x, y, label.split(".", 2)[0])
        ### add function to output the pls-da plot as .png file
        if title_name is not None:
            plt.savefig("./results/" + title_name + ".png", dpi=300)

        plt.show()
