# Fab Expense Analyzer

This is a simple expense analyzer for First Abu Dhabi Banks statements.

1. Download your transactions history
2. Define your mapping of merchant names to categories
3. Run the script and get a report of your expenses per card and in total

# Usage

### 1. Download repo

```git clone https://github.com/ppokrovskii/Fab_Expense_Analyzer```

### 2. Download transactions from FAB online banking

*Credit Cards -> Select your card -> Filter transactions -> Download Transactions -> Download as CSV*

You can download statements for multiple cards if you want

### 3. Store it in _Fab_Expense_Analyzer/source_data_ folder

### 4. Define your mapping

open _categories.py_ in your favorite editor and define your mapping using regex

### 5. Run the script

Open command line in Fab_Expense_Analyzer and run the script

```python main.py```

### Get result in _output_ folder with the following files:

1. <source_file_name> - proper csv with categories as it should come from FAB itself
2. <source_file_name>_grouped.csv - grouped by category sums of Debit Amounts
3. total_grouped.csv - grouped by category sums of Debit Amounts for source files

# Prerequisites

* Python 3.10
* Dependencies installed using ```pip install requirements.txt```
