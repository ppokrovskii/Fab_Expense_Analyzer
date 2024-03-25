import argparse
from pathlib import Path

import pandas as pd

from csv_cleaner import clean_csv
from data_processing import group_df, split_df_by_month, split_by_week
from utils import bcolors, df_to_csv

try:
    from categories import categories
except ModuleNotFoundError:
    # check if sample_categories.py exists
    if Path('sample_categories.py').exists():
        print(f'{bcolors.FAIL}Please rename sample_categories.py to categories.py{bcolors.ENDC}')
    else:
        print(f'{bcolors.FAIL}Please create categories.py file with categories dictionary{bcolors.ENDC}')
    exit(1)

# read args split by month (True/False, default=True)
parser = argparse.ArgumentParser()
parser.add_argument('--split_by_month', default='True')
parser.add_argument('--first_day_of_month', default=1)
args = parser.parse_args()
split_by_month = args.split_by_month.lower() == 'true'
first_day_of_month = int(args.first_day_of_month)

base_dir = Path(__file__).parent
source_data_dir = base_dir / 'source_data'
output_dir = base_dir / 'output'
# create output dir if it does not exist
output_dir.mkdir(parents=True, exist_ok=True)

# function that cleans up csv file: remove lines that start with empty values
# and remove lines that have only one value

if __name__ == '__main__':
    total_df = pd.DataFrame()
    # iterate over files in source_data_dir
    for source_file in source_data_dir.iterdir():
        target_file = output_dir / source_file.name
        try:
            clean_csv(output_dir, source_file)
        except PermissionError:
            print(f'{bcolors.FAIL}PermissionError: Please close {source_file.name} file{bcolors.ENDC}')
            exit(1)
        # read csv to dataframe
        df = pd.read_csv(target_file)
        print(df.head())
        df_to_csv(df, output_dir / target_file.name, index=False)
        # add dataframe to total_df using concat
        total_df = pd.concat([total_df, df])
        grouped_df = group_df(df)
        # store grouped_df to csv file
        df_to_csv(grouped_df, output_dir / source_file.name.lower().replace('.csv', '_grouped.csv'))
    # split grouped_df by month
    if split_by_month:
        split_df_by_month(total_df, output_dir, first_day_of_month=first_day_of_month)
    split_by_week(total_df, output_dir, first_day_of_month=first_day_of_month)
    grouped_df = group_df(total_df)

    df_to_csv(grouped_df, output_dir / 'total_grouped.csv')
