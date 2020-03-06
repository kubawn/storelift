import pytest
from src.cli import parse
from src.commands import create


def test_parse_method():
    assert parse("create 10 10") == [create, 10, 10.0]
    assert parse("abc") == None
    assert parse("create 10 a") == None
    