import pandas as pd

df = pd.read_csv(
    "/Users/ericliao/Desktop/compare_similarity_score_between_original_and_new/new study/new_modified/prescreen_threshold_500_query_8_to_library_15_matches_rank.csv",
    header=0)

rank_list = [1, 3, 5, 10, 20, 50]
for i in rank_list:
    df_rank = df[df['Rank'] <= i]
    df_rank = df_rank.dropna(axis=0, subset=['Score Original'])

    rank_prescreen_df = df_rank['Score Prescreen']
    numerator_prescreen = rank_prescreen_df[rank_prescreen_df != ''].dropna().index.size

    denominator_original = df_rank.index.size

    inclusion_rate = numerator_prescreen / denominator_original

    print("inclusion rate of Rank " + str(i) + " is: " + str(inclusion_rate) + "\n")
