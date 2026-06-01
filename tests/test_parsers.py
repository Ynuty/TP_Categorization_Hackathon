import pytest
from pathlib import Path

from mail_system.models import Category, Email
from mail_system.parser import EmailParser, ParseError
from mail_system.classificator import RuleBaseClassificator


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def parser():
    return EmailParser()


@pytest.fixture
def classifier():
    return RuleBasedClassifier()


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
    

def test_spam_email(classificator, parser):
    path = FIXTURES / "spam.txt"

    email = parser.parse(path)
    result = classificator.classify(email)

    assert result.category == Category.SPAM
    assert result.reason == "похоже на спам или фишинг"
