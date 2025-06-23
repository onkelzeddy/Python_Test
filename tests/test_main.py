import pytest

from main import create_parser


@pytest.fixture
def command_line_args(monkeypatch):
    def set_args(arg_list):
        parser = create_parser()
        args = parser.parse_args(arg_list)
        return args

    return set_args


def test_with_args(command_line_args):
    args = command_line_args(
        ["--file", "default.csv", "--where", "brand=xiaomi", "--aggregate", "price=avg"]
    )
    assert args.file == "default.csv"
    assert args.where == "brand=xiaomi"
    assert args.aggregate == "price=avg"


def test_with_default_age(command_line_args):
    args = command_line_args(["--file", "default.csv"])
    assert args.file == "default.csv"
    assert args.where is None
    assert args.aggregate is None
