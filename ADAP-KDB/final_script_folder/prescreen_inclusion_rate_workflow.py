import pandas as pd
import numpy as np

df_original = pd.read_csv(
    "/Users/ericliao/Desktop/manuscript_revise/High_Intensity/match_results/original_high_res.csv", header=0)

df_prescreen = pd.read_csv(
    "/Users/ericliao/Desktop/manuscript_revise/High_Intensity/match_results/prescreen_threshold_50_query_16_to_library_16_matches_high.csv",
    header=0)

output_folder = "/Users/ericliao/Desktop/manuscript_revise/High_Intensity/compare_results/new_compare/"
output_combine_name = "prescreen_threshold_50_query_16_to_library_16_matches_combine.csv"
output_rank_name = "prescreen_threshold_50_query_16_to_library_16_matches_rank.csv"

number_of_spectra = df_original["Query Spectrum ID"].unique().size

df_original = df_original.dropna()
df_prescreen = df_prescreen.dropna()

df_combine = pd.merge(df_original, df_prescreen, on=["Query Spectrum ID", "Match Spectrum ID"], how="outer")

df_combine.rename(columns={"Score_x": "Score Original", "Score_y": "Score Prescreen"}, inplace=True)

df_combine.to_csv(output_folder + output_combine_name)

####### step 2
pd.set_option('precision', 15)

# df_original_without_new_score = df_combine[(df_combine['Score Original'].notnull())
#                                            & (df_combine['Score Prescreen'].isnull())]
#
# df_original = df_original_without_new_score[['Score Original']]
#
# df_both_scores = df_combine[['Score Original', 'Score Prescreen']].dropna()

df_original_score_greater_600 = df_combine[(df_combine['Score Original'] >= 0.6)
                                           & (df_combine['Score Prescreen'] >= 0.6)]

df_original_original_great_600_prescreen_nan = df_combine[(df_combine['Score Original'] >= 0.6) & (df_combine['Score Prescreen'].isna())]

df_combine = df_original_score_greater_600.append(df_original_original_great_600_prescreen_nan)

df_combine.sort_values(['Query Spectrum ID', "Score Original"], ascending=[True, False])
df_combine['Rank'] = np.nan
query_spectrum_id = 0
count = 0



## REMEMBER TO CHANGE THE NUMBER IN range() for different msp file
for i in range(number_of_spectra):
    df_combine.loc[df_combine['Query Spectrum ID'] == i, 'Rank'] = range(1, 1 + len(
        df_combine[df_combine['Query Spectrum ID'] == i]))
    # df_combine[df_combine['Query Spectrum ID'] == i]['Rank'] = range(1, 1 + len(
    #     df_combine[df_combine['Query Spectrum ID'] == i]))

df_combine.to_csv(output_folder + output_rank_name)

####### step 3

rank_list = [1, 3, 5, 10, 20, 50]
for i in rank_list:
    df_rank = df_combine[df_combine['Rank'] <= i]
    df_rank = df_rank.dropna(axis=0, subset=['Score Original'])

    rank_prescreen_df = df_rank['Score Prescreen']
    numerator_prescreen = rank_prescreen_df[rank_prescreen_df != ''].dropna().index.size

    denominator_original = df_rank.index.size

    inclusion_rate = numerator_prescreen / denominator_original

    print("inclusion rate of Rank " + str(i) + " is: " + str(inclusion_rate) + "\n")
