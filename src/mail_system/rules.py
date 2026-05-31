import re

from .models import Category


class Rule:
    def __init__(self, category, pattern, reason):
        self.category = category
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.reason = reason
