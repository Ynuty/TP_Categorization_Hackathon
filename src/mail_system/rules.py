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
        r"выиграл|iphone|лотере|крипт|заблокирован|click here|бесплатн|зараб|бонус|"
        r"инвест|доход|переходи",
        "похоже на спам или фишинг"        
    ),
    Rule(
        Category.MONITORING,
        r"ALERT:|healthcheck|grafana|jira\.internal|monitoring\.internal|"
        r"автоматическ|noreply@jira|\[INFO\].*healthcheck",
        "авто-уведомление от системы",
    ),
    Rule(
        Category.INCIDENTS,
        r"не работает|не отвечает|сбой|критич|зависает|не открывается|"
        r"не запускается|URGENT|ERR_\d+|помощь"
        "срочное обращение или инцидент",
    ),
    Rule(
        Category.ACCESS,
        r"доступ|vpn|учетн|парол|логин|права доступа|разрешени|"
        "запрос доступа"
    ),
    Rule(
        Category.SOFTWARE,
        r"установ|обнов|chrome|adobe|excel|zoom|reader|программ|"
        r"приложени|лицензи",
        "установка или обновление ПО",
    ),
    Rule(
        Category.GENERAL,
        r"^Re:|^Fwd:|переслал|напоминан|отпуск|согласован|вопрос",
        "обычное обращение",
    ),
]
