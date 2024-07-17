import pandas as pd

csf_df = pd.read_csv('/Lab_work/data_files/HMDB_sample_files/csv_files/csf_metabolites.csv',
                     header=0, index_col=False)
feces_df = pd.read_csv('/Lab_work/data_files/HMDB_sample_files/csv_files/feces_metabolites.csv',
                       header=0, index_col=False)
saliva_df = pd.read_csv('/Lab_work/data_files/HMDB_sample_files/csv_files/saliva_metabolites.csv',
                        header=0, index_col=False)
serum_df = pd.read_csv('/Lab_work/data_files/HMDB_sample_files/csv_files/serum_metabolites.csv',
                       header=0, index_col=False)
sweat_df = pd.read_csv('/Lab_work/data_files/HMDB_sample_files/csv_files/sweat_metabolites.csv',
                       header=0, index_col=False)
urine_df = pd.read_csv('/Lab_work/data_files/HMDB_sample_files/csv_files/urine_metabolites.csv',
                       header=0, index_col=False)

name_list = ['CSF', 'Feces', 'Saliva', 'Serum', 'Sweat', 'Urine']

df_list = [csf_df, feces_df, saliva_df, serum_df, sweat_df, urine_df]

for df, name, index in zip(df_list, name_list, range(len(df_list))):
    df_rest_list = []
    for number in range(len(df_list)):
        if number != index:
            df_rest_list.append(df_list[number])
    df_rest = pd.concat(df_rest_list)
    df_left = df.loc[:, ['accession']]
    df_right = df_rest.loc[:, ['accession']]
    # df_unique = df_left.merge(df_right, how='outer', indicator=True).set_index('index').loc[lambda x: x['_merge'] == 'left_only']
    df_unique = df_left.reset_index().merge(df_right,
                                            how='outer',
                                            indicator=True).set_index('index').loc[lambda x: x['_merge'] == 'left_only']
    df_unique_whole = df.loc[df_unique.index.values].reset_index(drop=True)

    df_unique_whole.to_csv('/Users/yliao13/phd_class_code/data_files/HMDB_sample_files/csv_files/' + name + '_unique_from_6_samples.csv')

