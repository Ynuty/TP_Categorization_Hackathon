import re

from .models import Category


class Rule:
    def __init__(self, category, pattern, reason):
        self.category = category
        self.pattern = re.compile(pattern, re.IGNORECASE) # IgnorCase - не смотреть на регистр букв
        self.reason = reason



RULES = [
    Rule(
        Category.SPAM, 
        r"выиграл|лотере|крипт|заблокирован|бесплатн|зараб|бонус|"
        r"инвест|доход|переходи|приз|казин|ставк",
        "похоже на спам или фишинг",        
    ),
    Rule(
        Category.MONITORING,
        r"ALERT:|healthcheck|grafana|jira\.internal|monitoring\.internal|"
        r"автоматическ|noreply@jira|\[INFO\].*healthcheck",
        "авто-уведомление от системы",
    ),
    Rule(
        Category.INCIDENTS,
        r"не работает|не отвечает|сбой|критич|срочно|ошибк|зависает|"
        r"не открывается|не запускается|сломал|замен|error|исключение|"
        r"инцидент|авария|недоступ|баг|упал|не функциониру",
        "срочное обращение или инцидент",
    ),
    Rule(
        Category.ACCESS,
        r"доступ|vpn|учетн|парол|логин|права доступа|разрешени|",
        "запрос доступа",
    ),
    Rule(
        Category.SOFTWARE,
        r"установ|обнов|chrome|adobe|excel|zoom|reader|программ|"
        r"приложени|лицензи|софт|драйвер",
        "установка или обновление ПО",
    ),
    Rule(
        Category.FINANCE,
        r"счет|счёт|оплат|платеж|налог|зарпл|банк|бюджет",
        "счета и уведомления об оплате",
    ),
        Rule(
        Category.DOCUMENTATION,
        r"инструкц|договор|документ|подтвердить|руководство",
        "документация",
    ),
        Rule(
        Category.MEETINGS,
        r"созвон|встреч|встретиться|обсудить|планерк",
        "встречи или созвоны",
    ),
    Rule(
        Category.GENERAL,
        r"^Re:|^Fwd:|переслал|напоминан|отпуск|согласован|вопрос",
        "обычное обращение",
    ),
]
