# Fab Expense Analyzer

This is a simple expense analyzer for First Abu Dhabi Banks statements.

1. Download your transactions history
2. Define your mapping of merchant names to categories
3. Run the script and get a report of your expenses per card and in total

# Usage

### 1. Download repo

```git clone https://github.com/ppokrovskii/Fab_Expense_Analyzer```

### 2. Download transactions from FAB online banking

```Credit Cards -> Select your card -> Filter transactions -> Download Transactions -> Download as CSV```

You can download statements for multiple cards if you want

Create folder ```Fab_Expense_Analyzer/source_data``` folder and store your downloaded csv files there

### 3. Install dependencies

```pip install requirements.txt```

### 4. Define your categories

rename ```sample_categories.py``` into ```categories.py```, open it and define your mapping (regex syntax is used)

### 5. Run the script

```python main.py --first_day_of_month=24```
#### parameters
```--first_day_of_month``` - optional parameter, equals to 1 by default. If you want to group transactions from salary day to
salary day then pass your salary day
```--split_by_month``` - optional parameter, equals to True by default. pass ```--split_by_month=False``` if you don't want
the split

### 6. Get result in ```output``` folder with the following files:

1. ```<source_file_name>``` - proper csv with categories as it should come from FAB itself
2. ```<source_file_name>_grouped.csv``` - grouped by category sums of Debit Amounts
3. ```total_grouped.csv``` - grouped by category sums of Debit Amounts for source files

# Prerequisites

* Python 3.10
