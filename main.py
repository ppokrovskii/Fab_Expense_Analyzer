from pathlib import Path

import pandas as pd

from categories import categories

base_dir = Path(__file__).parent
source_data_dir = base_dir / 'source_data'
output_dir = base_dir / 'output'
# create output dir if it does not exist
output_dir.mkdir(parents=True, exist_ok=True)


# function that cleans up csv file: remove lines that start with empty values
# and remove lines that have only one value
def clean_csv(filename):
    skip_header = True
    with open(filename, 'r') as f:
        lines = f.readlines()
    result_file = output_dir / Path(filename).name
    with open(result_file, 'w') as f:
        for line in lines:
            if line.startswith(','):
                continue
            if line.count(',') == 0:
                continue
            if line.startswith('Posting'):
                if skip_header:
                    skip_header = False
                else:
                    continue
            if line.find(',,') <= 12:
                for i in range(2):
                    line = line.replace(',,', ',')
            else:
                line = line.replace(',,', ',')
            # trim commas at the end and add new line character
            line = line.rstrip().rstrip(',') + '\n'
            #
            # line = line.replace(',,,', ',')
            f.write(line)


def add_categories(dataframe):
    # add column 'category' to dataframe
    dataframe['category'] = dataframe['Description'].replace(categories, regex=True)
    # tag equal description replace tag with 'Other'
    dataframe['category'] = dataframe['category'].where(~(dataframe['category'] == dataframe['Description']), 'Other')
    return dataframe


# main
total_df = pd.DataFrame()


def group_df(df):
    # created grouped_df with sums of Debit Amount by category
    grouped_df = df.groupby('category')['Debit Amount'].sum()
    # sort grouped_df by Debit Amount
    grouped_df = grouped_df.sort_values(ascending=False)
    return grouped_df


for source_file in source_data_dir.iterdir():
    target_file = output_dir / source_file.name
    clean_csv(source_file)
    # read csv to dataframe
    df = pd.read_csv(target_file)
    df = add_categories(df)
    print(df.head())
    df.to_csv(output_dir / target_file.name, index=False)
    # add dataframe to total_df using concat
    total_df = pd.concat([total_df, df])
    grouped_df = group_df(df)
    # store grouped_df to csv file
    grouped_df.to_csv(output_dir / source_file.name.lower().replace('.csv', '_grouped.csv'))

grouped_df = group_df(total_df)
# store grouped_df to csv file
grouped_df.to_csv(output_dir / 'total_grouped.csv')
