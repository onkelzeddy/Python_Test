import sys

import pytest

from main import arg_parse
from utils.args_validator import validate


def test_with_right_args(monkeypatch):
    test_args = [
        "prog",
        "--file",
        "/home/mishka-sosiska/Workspace/Python_Test/tests/tests_utils_files/products.csv",
        "--where",
        "brand=xiaomi",
        "--aggregate",
        "price=avg",
    ]

    monkeypatch.setattr(sys, "argv", test_args)

    args = arg_parse()

    assert (
        args.file
        == "/home/mishka-sosiska/Workspace/Python_Test/tests/tests_utils_files/products.csv"
    )
    assert args.where == "brand=xiaomi"
    assert args.aggregate == "price=avg"
    assert validate(args)


def test_with_wrong_where_arg(monkeypatch):
    test_args = [
        "prog",
        "--file",
        "/home/mishka-sosiska/Workspace/Python_Test/tests/tests_utils_files/products.csv",
        "--where",
        ">xiaomi",
        "--aggregate",
        "price=avg",
    ]

    monkeypatch.setattr(sys, "argv", test_args)

    args = arg_parse()

    assert (
        args.file
        == "/home/mishka-sosiska/Workspace/Python_Test/tests/tests_utils_files/products.csv"
    )
    assert args.where == ">xiaomi"
    assert args.aggregate == "price=avg"
    with pytest.raises(ValueError, match="Invalid WHERE clause"):
        validate(args)


def test_with_wrong_file_arg(monkeypatch):
    test_args = [
        "prog",
        "--file",
        "/home/mishka-sosiska/Workspace/Python_Test/tests/tests_utils_files",
        "--where",
        "brand>xiaomi",
        "--aggregate",
        "price=avg",
    ]

    monkeypatch.setattr(sys, "argv", test_args)

    args = arg_parse()

    assert (
        args.file
        == "/home/mishka-sosiska/Workspace/Python_Test/tests/tests_utils_files"
    )
    assert args.where == "brand>xiaomi"
    assert args.aggregate == "price=avg"
    with pytest.raises(
        ValueError, match="Invalid file path or not csv file was provided"
    ):
        validate(args)
