# Author: Eric Liao
# August 2021

"""
This PLS-DA will be able to apply 2 components analysis on a dataset.
The functions also include calculating VIPs, Q2 score and Plot a 2D pls-da plot based on targets.

how to use this function: in the configuration, at the Parameters section,
    filled with: --input_file=here_insert_file_directory --target_type_number=integer_number_here [--axis=0_or_1_defualt_as 0]

This function needs three inputs:
    1. The dataset (detail information check the help in argument --input_file) **required
    2. The number of classes/ targets this dataset has **required
    3. A axis parameter tell the module the structure of your data
        (detailed information see the help in argument --axis) not required, if not provided, then axis=0
"""

import argparse
import pandas as pd
from Lab_work.PLS_DA_for_2_components.create_target_dummy_matrix import (
    create_target_dummy_matrix,
)
from Lab_work.PLS_DA_for_2_components.pls_da import pls_da_model
from Lab_work.PLS_DA_for_2_components.pls_da_2d_plot import plot_2d
from Lab_work.PLS_DA_for_2_components.vips import vips
from Lab_work.PLS_DA_for_2_components.Q2_for_each_target import calculate_q2


def main():
    parser = argparse.ArgumentParser(description="passing parameters")
    parser.add_argument(
        "--input_file",
        help="files contains only samples and features information, either csv/txt,"
        "if axis = 0, first row is the feature names, "
        "index column is sample/target names;"
        "if axis = 1, first row is sample/target names,"
        "index column is feature names or just index number.",
        required=True,
    )

    parser.add_argument(
        "--target_type_number",
        type=int,
        help="Provide the number of classes/targets",
        required=True,
    )

    parser.add_argument(
        "--axis",
        nargs="?",
        const=1,
        type=int,
        default=0,
        help="axis value will be integer number(0 or 1), default is 0, "
        "if axis = 0, the structure of dataset is rows as samples, columns as features; "
        "if axis = 1, the structure of dataset is rows as features, columns as samples."
        "The example of dataset with axis=0 and axis=1 is in the folder called data_file_example",
    )
    args = parser.parse_args()

    input_file = args.input_file
    target_type_number = args.target_type_number
    axis = args.axis

    ########## get data from csv file######################

    if axis == 1:
        df = pd.read_csv(input_file, header=None, index_col=0)
        target_list = df.iloc[0, 0:].tolist()

    if axis == 0:
        df = pd.read_csv(input_file, header=0, index_col=0)
        target_list = df.index.tolist()
    #######################################################

    ########## create target for pls-da ###################
    if target_type_number == 2:
        target_info = create_target_dummy_matrix.target_2_classes(target_list)

    if target_type_number > 2:
        target_info = create_target_dummy_matrix.target_multi_classes(
            target_list, target_type_number
        )

    target = target_info[0]
    target_color = target_info[1]
    target_names = target_info[2]
    #######################################################

    ########## build plsda model using sklearn pls-regression####
    plsr = pls_da_model.pls_da(df, target, axis)
    #############################################################

    ########## calculate VIPs vector ######################
    vip_list = vips.vips(plsr)
    print(vip_list)
    #######################################################

    ######### print out the q2 with leave one out cross-validation #####
    calculate_q2.calculate_q2(df, target, target_type_number, axis)
    ####################################################################

    ######### scores: The scores describe the position of
    ### each sample in each determined latent variable (LV)####
    scores = pd.DataFrame(plsr.x_scores_).to_numpy()
    ###############################################################

    plot_2d.plsda_2d_plot(scores, target_color, target_names, target_type_number)


if __name__ == "__main__":
    main()
