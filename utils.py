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


def df_to_csv(df_to_store, file, index=True):
    # store grouped_df to csv file

    try:
        df_to_store.to_csv(file, index=index)
    except PermissionError:
        print(f'{bcolors.FAIL}PermissionError: Please close {file.name} file{bcolors.ENDC}')
        exit(1)
