from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

from utils import df_to_csv, bcolors


def group_df(df):
    # convert Debit Amount to float using .loc
    # df.loc[:, 'Debit Amount'] = df['Debit Amount'].astype(float)

    # created grouped_df with sums of Debit Amount by category
    grouped_df = df.groupby('Category')['Debit Amount'].sum()
    # sort grouped_df by Debit Amount
    grouped_df = grouped_df.sort_values(ascending=False)
    return grouped_df


# function that splits grouped_df by month and store them into split_by_month directory.
# function should take day of month as  a parameter and split grouped_df by month
# and store them into split_by_month directory.
def split_df_by_month(df, output_dir, first_day_of_month=1):
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
    # parse date from formar 23/03/2024 but trim first
    df['date'] = pd.to_datetime(df['Posting Date'], format='%Y-%m-%d')
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


def split_by_week(df, output_dir, first_day_of_month=1):
    # create split_by_month directory
    split_by_month_dir = output_dir / 'split_by_week'
    # delete all files in split_by_month directory
    split_by_month_dir.mkdir(parents=True, exist_ok=True)
    for file in split_by_month_dir.iterdir():
        try:
            file.unlink()
        except PermissionError:
            print(f'{bcolors.FAIL}PermissionError: Please close {file.name} file{bcolors.ENDC}')
            exit(1)
    # create dataframe with month and year
    # parse date from formar 23/03/2024 but trim first
    df['date'] = pd.to_datetime(df['Posting Date'], format='%Y-%m-%d')
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
