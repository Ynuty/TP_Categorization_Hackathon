import pytest
from pathlib import Path

from mail_system.models import Category
from mail_system.parsers import EmailParser
from mail_system.classificator import RuleBaseClassificator

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def parser():
    return EmailParser()


@pytest.fixture
def classificator():
    return RuleBaseClassificator()

def test_spam_email(classificator, parser):
    path = FIXTURES / "spam.txt"

    email = parser.parse(path)
    result = classificator.classify(email)

    assert result.category == Category.SPAM
    assert result.reason == "похоже на спам или фишинг"

def test_unclassified_email(parser, classificator):
    email = parser.parse(FIXTURES / "unclassified.txt")
    result = classificator.classify(email)

    assert result.category == Category.UNCLASSIFIED


