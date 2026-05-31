import shutil
import zipfile
from pathlib import Path
from .models import Category

def ensure_mailbox_layout(mailbox_root: Path) -> None:  # создание структуры папок (если ее еще нет)
    mailbox_root.mkdir(parents=True, exist_ok=True)  # добавление папки и родителей (или не вызывать ошибку, если уже существует)
    (mailbox_root / "inbox").mkdir(exist_ok=True)
    for category in Category:  # папка для каждой категории из models.py вызывается из main.py перед обработкjq
        (mailbox_root / category.value).mkdir(exist_ok=True)

def unique_dest_path(dest_dir: Path, filename: str) -> Path:  # обработка повторяющихся имен
    dest = dest_dir / filename
    if not dest.exists():
        return dest

    stem = dest.stem  # имя без разрешения
    suffix = dest.suffix  # добавление расширениня .txt для нового наименования
    counter = 1
    while True:
        candidate = dest_dir / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1