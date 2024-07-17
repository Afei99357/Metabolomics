# Author: Eric Liao
# August 2021

from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd


class pls_da_model:
    def pls_da(df, target, axis):
        scaler = StandardScaler()
        ## axis == 0, the structure of df is rows as samples, columns as features
        ## axis == 1, the structure of df is rows as features, columns as samples
        if axis == 0:
            #### pre-processing data###
            df = pd.DataFrame(scaler.fit_transform(df)).values
            ####### PLS-DA ########
            plsr = PLSRegression(n_components=2, scale=False)
            plsr.fit(df, target)
            #######################
        else:
            ## remove the first row which is target names
            df = df.iloc[1:, :]
            df_transpose = df.T
            #### pre-processing data###
            df_transpose = pd.DataFrame(scaler.fit_transform(df_transpose)).values
            ####### PLS-DA ########
            plsr = PLSRegression(n_components=2, scale=False)
            plsr.fit(df_transpose, target)
            #######################

        return plsr
