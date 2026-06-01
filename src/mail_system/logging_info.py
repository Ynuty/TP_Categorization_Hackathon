import logging 
from pathlib import Path


def logs_creator(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True) #create папку если еще нет

    logger = logging.getLogger("mail_system") #особенность библиотеки - один логгер для всего
    logger.setLevel(logging.INFO) # пропускаем не все, только INFO и ERROR (есть еще DEBUG - полная отладка))
    logger.handlers.clear() # чистим старые обработчики, чтобы логи не повторялись

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger