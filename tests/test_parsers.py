import pytest
from pathlib import Path

from mail_system.parser import EmailParser, ParseError


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def parser():
    return EmailParser()


def test_empty_file(parser):
    path = FIXTURES / "empty.txt"

    with pytest.raises(ParseError):
        parser.parse(path)


def test_valid_json(parser):
    path = FIXTURES / "valid.json"
    email = parser.parse(path)

    assert email.sender == "test@company.ru"
    assert email.subject == "test"
    assert email.body == "hello"


def test_broken_json(parser):
    path = FIXTURES / "broken.json"

    with pytest.raises(ParseError):
        parser.parse(path)


def test_binary_file(parser):
    path = FIXTURES / "binary.bin"

    with pytest.raises(ParseError):
        parser.parse(path)

    


