import argparse
import json
import pandas as pd
import os


def main():
    parser = argparse.ArgumentParser(description="passing parameters")
    parser.add_argument('--input', help="directory of studies", required=True)
    parser.add_argument('--output', help="output directory", required=True)

    args = parser.parse_args()

    input_directory = args.input
    output_directory = args.output

    columns_list = ['Study ID', 'Study Summary', 'Sample Source', 'Species', 'disease']
    meta_df = pd.DataFrame(columns=columns_list)

    for root, subdirectories, files in os.walk(input_directory):
        for file in files:
            if file == "meta.json":
                meta_file = open(os.path.join(root, file), )
                meta_dic = json.load(meta_file)
                new_row = {'Study ID': meta_dic['url'].split('StudyID=', 1)[1],
                           'Study Summary': meta_dic['study_summary'],
                           'Sample Source': meta_dic['tags']['sample source'],
                           'Species': meta_dic['tags']['species (common)'],
                           'disease': meta_dic['tags']['disease']}
                meta_df = meta_df.append(new_row, ignore_index=True)

    meta_df.to_csv(os.path.join(output_directory, 'metabolomics_workbench_studies_info.csv'))


if __name__ == '__main__':
    main()
