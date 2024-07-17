import argparse

import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="compare difference between urine and serum")
    parser.add_argument('--input_serum', help='serum csv file', required=True)
    parser.add_argument('--input_urine', help='urine csv file', required=True)
    args = parser.parse_args()

    serum_csv = args.input_serum
    urine_csv = args.input_urine

    serum_df = pd.read_csv(serum_csv, header=0, index_col=False)
    urine_df = pd.read_csv(urine_csv, header=0, index_col=False)

    serum_accession_name_df = serum_df.loc[:, ('accession', 'name')]
    urine_accession_name_df = urine_df.loc[:, ('accession', 'name')]

    serum_only_accession_name_df = serum_accession_name_df.reset_index().merge(urine_accession_name_df,
                     how='outer', indicator=True).set_index('index').loc[lambda x: x['_merge'] == 'left_only']
    urine_only_df_accession_name_df = urine_accession_name_df.reset_index().merge(serum_accession_name_df,
                     how='outer', indicator=True).set_index('index').loc[lambda x: x['_merge'] == 'left_only']

    common_df = pd.merge(serum_df, urine_df, how='inner', on=['accession', 'name'])
    serum_only_df = serum_df.iloc[serum_only_accession_name_df.index.values]
    urine_only_df = urine_df.iloc[urine_only_df_accession_name_df.index.values]

    df3 = pd.merge(serum_df, urine_df,  how='outer', left_on=['accession', 'name'], right_on=['accession', 'name'])

    common_df.to_csv('/Users/yliao13/phd_class_code/data_files/HMDB_sample_files/common_urine_serum.csv')
    serum_only_df.to_csv('/Users/yliao13/phd_class_code/data_files/HMDB_sample_files/serum_unique_metabolites.csv')
    urine_only_df.to_csv('/Users/yliao13/phd_class_code/data_files/HMDB_sample_files/urine_unique_metabolites.csv')

if __name__ == '__main__':
    main()