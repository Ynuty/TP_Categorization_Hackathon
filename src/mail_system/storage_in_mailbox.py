import shutil
import zipfile
from pathlib import Path
from .models import Category

def ensure_mailbox_layout(mailbox_root: Path) -> None:  # создание структуры папок (если ее еще нет)
    mailbox_root.mkdir(parents=True, exist_ok=True)  # добавление папки и родителей (или не вызывать ошибку, если уже существует)
    (mailbox_root / "inbox").mkdir(exist_ok=True)
    for category in Category:  # папка для каждой категории из models.py вызывается из main.py перед обработкjq
        (mailbox_root / category.value).mkdir(exist_ok=True)
