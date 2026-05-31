from .models import Category, ClassificationResult, Email
from .rules import RULES



class RuleBaseClassificator:
    def classify(self, email: Email) -> ClassificationResult:
        text = f"{email.subject}\n{email.body}\n{email.sender}" # тема -тело - отправитель


        for rule in RULES:
            if rule.pattern.search(text): # отсылает нас в класс RULES
                return ClassificationResult(

                    category=rule.category,
                    reason=rule.reason,
                )
            
        # если никуда не ушло -> либо наш косяк, либо потом определить в failed
        return ClassificationResult(
            category=Category.UNCLASSIFIED,
            reason="ничего не подошло",
        )
            

