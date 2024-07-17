"""Keeps matches with score >= 0.6 only."""

import argparse
import pandas as pd

from os.path import splitext


def filter_matches(filename: str):
    df = pd.read_csv(filename, header=0)
    df = df[df.Score >= 0.8]

    name, extension = splitext(filename)
    output_filename = name + '.filtered' + extension
    df.to_csv(output_filename, index=False)


if __name__ == '__main__':
    filter_matches('data/matches_2020-06-02.csv')
#     print('Original size:', len(df))
#     df = df[df.Score >= 0.6]
#     print('Filtered size:', len(df))

#     filtered_filename, extension = splitext(filename)
#     filtered_filename += '.filtered' + extension
#     df.to_csv(filtered_filename, index=False)


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Keeps matches with score >= 0.6 only')
#     parser.add_argument('--file', help='Path to CSV file containing matches', required=True)

#     args = parser.parse_args()
#     filter_matches(args.file)
