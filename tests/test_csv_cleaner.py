import csv
from datetime import datetime

from csv_cleaner import Record


def test_record():
    csv_line = '" 23/03/2024"," 22/03/2024",1999029235 - Instashop              Dubai         ARE,,46.80'
    csv_reader = csv.reader([csv_line])
    line = next(csv_reader)
    record = Record(*line)
    assert record.posting_date == datetime(2024, 3, 23)
    assert record.value_date == datetime(2024, 3, 22)
    assert record.description == '1999029235 - Instashop              Dubai         ARE'
    assert record.debit_amount == 0.0
    assert record.credit_amount == 46.80
    assert record.category == 'groceries'
    assert str(
        record) == '2024-03-23,2024-03-22,1999029235 - Instashop              Dubai         ARE,0.0,46.8,groceries'


def test_record_no_category():
    csv_line = '" 23/03/2024"," 22/03/2024",Other Category,,46.80'
    csv_reader = csv.reader([csv_line])
    line = next(csv_reader)
    record = Record(*line)
    assert record.category == 'Other'
    assert str(record) == '2024-03-23,2024-03-22,Other Category,0.0,46.8,Other'


def test_record_no_debit_amount():
    csv_line = '" 23/03/2024"," 22/03/2024",Other Category,,'
    csv_reader = csv.reader([csv_line])
    line = next(csv_reader)
    record = Record(*line)
    assert record.debit_amount == 0.0
    assert str(record) == '2024-03-23,2024-03-22,Other Category,0.0,0.0,Other'


def test_record_no_credit_amount():
    csv_line = '" 23/03/2024"," 22/03/2024",Other Category,46.80,'
    csv_reader = csv.reader([csv_line])
    line = next(csv_reader)
    record = Record(*line)
    assert record.credit_amount == 0.0
    assert str(record) == '2024-03-23,2024-03-22,Other Category,46.8,0.0,Other'
