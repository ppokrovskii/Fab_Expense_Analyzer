import csv
import logging
import re
from datetime import datetime
from pathlib import Path

from categories import categories


class Record:
    # Posting Date,Value date,Description,Debit Amount,Credit Amount,category
    def __init__(self, posting_date, value_date, description, debit_amount, credit_amount):
        # convert posting date from format 23/03/2024 to datetime but remove spaces from start and end
        self.posting_date = datetime.strptime(posting_date.strip(), '%d/%m/%Y')

        # convert value date from format 23/03/2024 to datetime
        self.value_date = datetime.strptime(value_date.strip(), '%d/%m/%Y')
        self.description = description
        # convert debit amount from format 79.00 to float or 0.0 if empty
        self.debit_amount = float(debit_amount.replace(',', '')) if debit_amount else 0.0
        # convert credit amount from format 79.00 to float or 0.0 if empty
        self.credit_amount = float(credit_amount.replace(',', '')) if credit_amount else 0.0

        # _categories = {key.lower(): value for key, value in categories.items()}
        # serch for category in categories when categories is a dict where key is a regex pattern and value is a category
        self.category = next(
            (value for key, value in categories.items() if re.search(key, self.description, re.IGNORECASE)), 'Other')

    def __str__(self):
        # format dates to DATE ISO format
        return f'{self.posting_date.date()},{self.value_date.date()},{self.description},{self.debit_amount},{self.credit_amount},{self.category}'


def clean_csv(output_dir, filename):
    lines_to_skip = 8
    result_file = output_dir / Path(filename).name
    with open(result_file, 'w') as result_f:
        # write header
        result_f.write('Posting Date,Value date,Description,Debit Amount,Credit Amount,Category\n')
        with open(filename, 'r') as source_f:
            csvreader = csv.reader(source_f)
            for line in csvreader:
                if lines_to_skip > 0:
                    lines_to_skip -= 1
                    continue
                try:
                    r = Record(*line)
                except ValueError:
                    logging.warning(f'Error parsing line: {line}')
                    continue
                result_f.write(f'{r}\n')
