# Author: Eric Liao
# August 2021

import numpy as np


class create_target_dummy_matrix:

    #### for target only has two types
    def target_2_classes(target_array):
        target = []
        target_color = []

        # get unique target class values
        unique_values = np.unique(target_array)

        for i in target_array:
            if str(i) == unique_values[0]:
                target.append(0)
                target_color.append(0)

            if str(i) == unique_values[1]:
                target.append(1)
                target_color.append(1)

        target = np.array(target)
        unique_values = np.array(unique_values)

        return [target, target_color, unique_values]

    #### for target has three types
    def target_multi_classes(target_array, target_type_number):

        sample_number = len(target_array)
        target = np.zeros(shape=(sample_number, target_type_number))
        target_color = []

        ## get unique target class values
        unique_values = np.unique(target_array)

        ## 3 classes target
        if target_type_number == 3:
            target_index = 0
            for i in target_array:
                if str(i) == str(unique_values[0]):
                    target[target_index] = [1, 0, 0]
                    target_color.append(0)
                if str(i) == str(unique_values[1]):
                    target[target_index] = [0, 1, 0]
                    target_color.append(1)
                if str(i) == str(unique_values[2]):
                    target[target_index] = [0, 0, 1]
                    target_color.append(2)
                target_index += 1

        ## 4 classes target
        if target_type_number == 4:
            target_index = 0
            for i in target_array:
                if str(i) == str(unique_values[0]):
                    target[target_index] = [1, 0, 0, 0]
                    target_color.append(0)
                if str(i) == str(unique_values[1]):
                    target[target_index] = [0, 1, 0, 0]
                    target_color.append(1)
                if str(i) == str(unique_values[2]):
                    target[target_index] = [0, 0, 1, 0]
                    target_color.append(2)
                if str(i) == str(unique_values[3]):
                    target[target_index] = [0, 0, 0, 1]
                    target_color.append(3)
                target_index += 1

        ## 5 classes target
        if target_type_number == 5:
            target_index = 0
            for i in target_array:
                if str(i) == str(unique_values[0]):
                    target[target_index] = [1, 0, 0, 0, 0]
                    target_color.append(0)
                if str(i) == str(unique_values[1]):
                    target[target_index] = [0, 1, 0, 0, 0]
                    target_color.append(1)
                if str(i) == str(unique_values[2]):
                    target[target_index] = [0, 0, 1, 0, 0]
                    target_color.append(2)
                if str(i) == str(unique_values[3]):
                    target[target_index] = [0, 0, 0, 1, 0]
                    target_color.append(3)
                if str(i) == str(unique_values[4]):
                    target[target_index] = [0, 0, 0, 0, 1]
                    target_color.append(4)
                target_index += 1

        return [target, target_color, unique_values]
