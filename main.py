import argparse

from childe_classes.csv_reader import CSV_Reader
from utils.args_validator import validate


def arg_parse():
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--file", type=str, required=True, help="csv file to parse")
    PARSER.add_argument(
        "--where", default=None, type=str, help="where clause to filter data"
    )
    PARSER.add_argument(
        "--aggregate", default=None, type=str, help="aggregate function to apply"
    )
    return PARSER.parse_args()


if __name__ == "__main__":
    ARGS = arg_parse()
    if validate(ARGS):
        csv_reader = CSV_Reader(ARGS.file, ARGS.where, ARGS.aggregate)
        csv_reader.read_and_print_csv_file()
