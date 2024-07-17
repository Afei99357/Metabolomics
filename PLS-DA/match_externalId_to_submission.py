import pandas as pd

df_need_match = pd.read_csv('/Users/ericliao/Desktop/similarity_study/study_0609/top_10_column_2_adap_kdb.csv', header=0, index_col=None)

df_match = pd.read_csv('/Users/ericliao/Desktop/similarity_study/study_0609/external_id_with_submission_id.csv', header=0, index_col=None)

df_match = df_match.dropna();

df_match_dict = df_match.set_index('id').to_dict()['ExternalId']

df_need_match["ExternalId"] = ""

for index, row in df_need_match.iterrows():
    submission_id = row['SubmissionId']
    if(submission_id in df_match_dict.keys()):
        df_need_match.loc[index, 'ExternalId'] = df_match_dict[submission_id]
    else:
        print(df_need_match.loc[index, 'ExternalId'])

df_need_match.to_csv('/Users/ericliao/Desktop/similarity_study/study_0609/top_10_column_2_adap_kdb_with_externalId.csv')
