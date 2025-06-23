import re
from argparse import Namespace

from utils.consts import AGGREGATE_FUNCS, AGGREGATE_REG_EXP, FILE_REG_EXP, WHERE_REG_EXP


def validate(args: Namespace):

    if re.match(FILE_REG_EXP, args.file) is None:
        raise ValueError("Invalid file path or not csv file was provided")

    if args.where is not None:
        if re.match(WHERE_REG_EXP, args.where) is None:
            raise ValueError("Invalid WHERE clause")

    if args.aggregate is not None:
        if re.match(AGGREGATE_REG_EXP, args.aggregate) is None:
            raise ValueError("Invalid aggregate function")
        elif args.aggregate.lower().split("=")[1] not in AGGREGATE_FUNCS:
            raise ValueError("Invalid aggregate function")

    return True
