# TP_Categorization_Hackathon
Система автоматической сортировки входящих писем по категориям на основе правил. Письма читаются из папки *inbox*, анализируются и раскладываются по "тематическим" подпапкам, находящимся в папке *mailbox*.

## Установка

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```powershell
python main.py
```

или через bash (Git Bash / WSL):

```bash
bash run.sh
```

Параметры:

```powershell
python main.py --mailbox mailbox --source data/inbox/inbox --force
```

- `--force` — очистить inbox и скопировать письма заново из source

## Результат

После запуска смотри:

- `mailbox/processing.log` — что куда попало и почему
- `mailbox/stats.txt` — сколько писем в каждой категории
- папки `mailbox/incidents/`, `mailbox/spam/` и т.д.

## Тесты

```powershell
pytest
```

Тесты используют файлы из `tests/fixtures/`, не из `data/inbox/`.


## Структура репозитория

```text
TP_Categorization_Hackathon/
├── main.py                        # Вход в программу, руководство для командной строки
├── requirements.txt               # Зависимости Python
├── pytest.ini                     # Настройки pytest
│
├── src/
│   └── mail_system/
│       ├── models.py              # Датаклассы: Email, Category, ClassificationResult, ProcessingStats
│       ├── parser.py              # Парсер писем различ. форматов
│       ├── classificator.py       # Rule-based классификатор
│       ├── rules.py               # Набор правил (регулярные выражения в категорию)
│       ├── main_process.py        # Оркестратор: читает inbox, классифицирует, перемещает в подпапки
│       ├── storage_in_mailbox.py  # Файловые операции: создание папок, перемещение, zip-распаковка
│       └── logging_info.py        # Настройка логгера (файл + консоль)
│
├── data/
│   ├── inbox/inbox/               # Исходные письма
│   ├── inbox.zip                  # Архив с теми же письмами (источник №2 — альтернатива)
│   └── TP_Hackathon.ipynb         # ТЗ
│
├── mailbox/                       # Результат работы (создаётся при запуске)
│   ├── inbox/                     # Временная папка — сюда копируются письма перед обработкой
│   ├── incidents/                 # Сбои, ошибки, критические обращения
│   ├── monitoring/                # Авто-уведомления от систем (Jira, Grafana, healthcheck)
│   ├── access/                    # Запросы доступа, VPN, пароли
│   ├── spam/                      # Спам и фишинг
│   ├── software/                  # Установка/обновление ПО
│   ├── finance/                   # Счета и платежи
│   ├── documentation/             # Документы, договоры, инструкции
│   ├── meetings/                  # Созвоны и встречи
│   ├── general/                   # Общие обращения
│   ├── unclassified/              # Письма, не подошедшие ни под одно правило
│   ├── failed/                    # Файлы, которые не удалось распарсить
│   ├── processing.log             # Подробный лог обработки каждого письма
│   └── stats.txt                  # Статистика по категориям
│
└── tests/
    ├── fixtures/                  # Тестовые файлы писем
    ├── test_classificator.py      # Тесты классификатора
    └── test_parsers.py            # Тесты парсера
```





**Классификация (classificator.py и rules.py):**
- RuleBaseClassificator получает объект Email и формирует единую строку поиска (тема - тело - отправитель)
- Далее последовательно из массива RULES проверяются паттерны и возвращается категория первого совпавшего (категории проверяются по возрастанию приоритетов)
- Список категорий и некоторых ключевых слов для каждой:
    1. spam (key words - )
    2. monitoring (key words - ALERT:, noreply@jira, автоматическ)
    3. incidents (key words - сбой, не работает, ошибк)
    4. access (key words - vpn, парол, логин)
    5. software (key words - обнов, программ, установ)
    6. finance (key words - зарпл, счет, платеж)
    7. documentation (key words - договор, подтвердить, инструкц)
    8. meetings (key words - созвон, встреч, планерк)
    9. general (key words - Re:, Fwd:, вопрос, согласован)


