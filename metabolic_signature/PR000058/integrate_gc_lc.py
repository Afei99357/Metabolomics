import pandas as pd

df_gc = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
                 "nist_mspepsearch_return/st000061_st000065.tsv", sep='\t', header=3, index_col=None)

df_lc = pd.read_csv("/Users/ericliao/PycharmProjects/Phd_Class/Lab_work/data_files/metabolomics_signature/"
                    "nist_mspepsearch_return/st000081_st000082.tsv", sep='\t', header=3, index_col=None)

df_gc