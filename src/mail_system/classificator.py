from .models import Category, ClassificationResult, Email
from .rules import RULES



class RuleBaseClassificator:
    def classify(self, email: Email) -> ClassificatorResalt:
        text = f"{email.subject}\n{email.body}\n{email.sender}"


        for rule in RULES:
            pass