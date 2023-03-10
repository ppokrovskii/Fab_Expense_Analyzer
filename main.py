import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd
from dateutil.relativedelta import relativedelta


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
parser.add_argument('--split_by_month', default=True)
parser.add_argument('--first_day_of_month', default=1)
args = parser.parse_args()
split_by_month = args.split_by_month.lower() == 'true'
first_day_of_month = int(args.first_day_of_month)

base_dir = Path(__file__).parent
source_data_dir = base_dir / 'source_data'
output_dir = base_dir / 'output'
# create output dir if it does not exist
output_dir.mkdir(parents=True, exist_ok=True)


def df_to_csv(df_to_store, file, index=True):
    # store grouped_df to csv file

    try:
        df_to_store.to_csv(file, index=index)
    except PermissionError:
        print(f'{bcolors.FAIL}PermissionError: Please close {file.name} file{bcolors.ENDC}')
        exit(1)


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
    # categories to lowercase for case-insensitive comparison
    global categories
    categories = {key.lower(): value for key, value in categories.items()}
    # add column 'category' to dataframe
    dataframe['category'] = dataframe['Description'].str.lower().replace(categories, regex=True)
    # tag equal description replace tag with 'Other'
    dataframe['category'] = dataframe['category'].where(
        ~(dataframe['category'] == dataframe['Description'].str.lower()), 'Other')
    dataframe['category'] = dataframe['category'].str.capitalize()
    return dataframe


def group_df(df):
    # created grouped_df with sums of Debit Amount by category
    grouped_df = df.groupby('category')['Debit Amount'].sum()
    # sort grouped_df by Debit Amount
    grouped_df = grouped_df.sort_values(ascending=False)
    return grouped_df


# function that splits grouped_df by month and store them into split_by_month directory.
# function should take day of month as  a parameter and split grouped_df by month
# and store them into split_by_month directory.
def split_df_by_month(df):
    # create split_by_month directory
    split_by_month_dir = output_dir / 'split_by_month'
    # delete all files in split_by_month directory
    split_by_month_dir.mkdir(parents=True, exist_ok=True)
    for file in split_by_month_dir.iterdir():
        try:
            file.unlink()
        except PermissionError:
            print(f'{bcolors.FAIL}PermissionError: Please close {file.name} file{bcolors.ENDC}')
            exit(1)
    # create dataframe with month and year
    df['date'] = pd.to_datetime(df['Posting Date'], format='%d/%m/%Y')
    # loop through dataframe and split by month
    start_date = df['date'].min()
    end_date = df['date'].max()
    next_month_start = datetime(start_date.year, start_date.month, first_day_of_month) + relativedelta(months=1)
    while next_month_start < end_date + relativedelta(months=1):
        # find rows where date is between start_date and next_month_start
        month_df = df[(df['date'] >= start_date) & (df['date'] < next_month_start)]
        # group month_df by category and sum Debit Amount
        grouped_df = group_df(month_df)
        df_to_csv(grouped_df, split_by_month_dir / f'{start_date.year}_{start_date.month}_{first_day_of_month}+.csv')
        start_date = next_month_start
        next_month_start = next_month_start + relativedelta(months=1)


# main
if __name__ == '__main__':
    total_df = pd.DataFrame()
    # iterate over files in source_data_dir
    for source_file in source_data_dir.iterdir():
        target_file = output_dir / source_file.name
        try:
            clean_csv(source_file)
        except PermissionError:
            print(f'{bcolors.FAIL}PermissionError: Please close {source_file.name} file{bcolors.ENDC}')
            exit(1)
        # read csv to dataframe
        df = pd.read_csv(target_file)
        df = add_categories(df)
        print(df.head())
        df_to_csv(df, output_dir / target_file.name, index=False)
        # add dataframe to total_df using concat
        total_df = pd.concat([total_df, df])
        grouped_df = group_df(df)
        # store grouped_df to csv file
        df_to_csv(grouped_df, output_dir / source_file.name.lower().replace('.csv', '_grouped.csv'))
    # split grouped_df by month
    if split_by_month:
        split_df_by_month(total_df)
    grouped_df = group_df(total_df)

    df_to_csv(grouped_df, output_dir / 'total_grouped.csv')
