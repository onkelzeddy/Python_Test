import csv

import pytest
from tabulate import tabulate

from childe_classes.csv_reader import CSV_Reader


def test_CSV_Reader_works_with_only_file_arg():
    csv_reader = CSV_Reader("tests/tests_utils_files/products.csv", None, None)
    table = csv.DictReader(open("tests/tests_utils_files/products.csv", "r"))
    assert tabulate(
        csv_reader.get_current_table_with_args_used(), headers="keys", tablefmt="psql"
    ) == tabulate(table, headers="keys", tablefmt="psql")


def test_CSV_Reader_works_with_where_arg_equal_text():
    csv_reader = CSV_Reader(
        "tests/tests_utils_files/products.csv", "brand=xiaomi", None
    )
    table = [
        {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
        {"name": "poco x5 pro", "brand": "xiaomi", "price": "299", "rating": "4.4"},
        {"name": "redmi 10c", "brand": "xiaomi", "price": "149", "rating": "4.1"},
    ]
    assert tabulate(
        csv_reader.get_current_table_with_args_used(), headers="keys", tablefmt="psql"
    ) == tabulate(table, headers="keys", tablefmt="psql")


def test_CSV_Reader_works_with_where_arg_more_text():
    csv_reader = CSV_Reader(
        "tests/tests_utils_files/products.csv", "brand>xiaomi", None
    )
    table = []
    assert tabulate(
        csv_reader.get_current_table_with_args_used(), headers="keys", tablefmt="psql"
    ) == tabulate(table, headers="keys", tablefmt="psql")


def test_CSV_Reader_works_with_where_arg_less_text():
    csv_reader = CSV_Reader(
        "tests/tests_utils_files/products.csv", "brand<xiaomi", None
    )
    table = [
        {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
        {
            "name": "galaxy s23 ultra",
            "brand": "samsung",
            "price": "1199",
            "rating": "4.8",
        },
        {"name": "iphone 14", "brand": "apple", "price": "799", "rating": "4.7"},
        {"name": "galaxy a54", "brand": "samsung", "price": "349", "rating": "4.2"},
        {"name": "iphone se", "brand": "apple", "price": "429", "rating": "4.1"},
        {
            "name": "galaxy z flip 5",
            "brand": "samsung",
            "price": "999",
            "rating": "4.6",
        },
        {"name": "iphone 13 mini", "brand": "apple", "price": "599", "rating": "4.5"},
    ]
    assert tabulate(
        csv_reader.get_current_table_with_args_used(), headers="keys", tablefmt="psql"
    ) == tabulate(table, headers="keys", tablefmt="psql")


def test_CSV_Reader_works_with_where_and_aggregate_args():
    csv_reader = CSV_Reader(
        "tests/tests_utils_files/products.csv", "price>500", "price=avg"
    )
    table = [{"avg": 919.0}]
    assert tabulate(
        csv_reader.get_current_table_with_args_used(), headers="keys", tablefmt="psql"
    ) == tabulate(table, headers="keys", tablefmt="psql")


def test_CSV_Reader_with_wrong_aggregate_arg():
    csv_reader = CSV_Reader("tests/tests_utils_files/products.csv", None, "brand=avg")
    with pytest.raises(ValueError, match="The column is not numeric"):
        csv_reader.get_current_table_with_args_used()
