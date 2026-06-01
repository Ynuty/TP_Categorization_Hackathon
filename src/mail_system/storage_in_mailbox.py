import shutil
import zipfile
from pathlib import Path
from .models import Category


#будем запускать после каждого запуска - полностью чистит mailbox
def clear_mailbox(mailbox_root: Path) -> None:
    mailbox_root = Path(mailbox_root)
    if mailbox_root.exists():
        shutil.rmtree(mailbox_root)


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

def move_file(src: Path, dest_dir: Path) -> Path:  # перемещает текущий файл в папку категории из inbox
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = unique_dest_path(dest_dir, src.name)  # изначатльно ставим файлу безопасное (unique) имя
    shutil.move(str(src), str(dest))
    return dest


def _flatten_nested_inbox(inbox_dir: Path) -> None:
    nested = inbox_dir / "inbox"
    if not nested.is_dir():
        return
    for path in nested.iterdir():
        if path.is_file() and not path.name.startswith("."):
            dest = unique_dest_path(inbox_dir, path.name)
            shutil.move(str(path), str(dest))
    if nested.exists() and not any(nested.iterdir()):
        nested.rmdir()


def extract_zip(zip_path: Path, mailbox_root: Path) -> None:
    mailbox_root.mkdir(parents=True, exist_ok=True)
    inbox_dir = mailbox_root / "inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(mailbox_root)
    _flatten_nested_inbox(inbox_dir)

def copy_inbox_files(source_dir: Path, inbox_dir: Path) -> int:  # копирует массив писем из источника в inbox
    inbox_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(source_dir.iterdir()):
        if path.is_file() and not path.name.startswith("."):  # благодаря .startswith() пропускаем скрытые файлы
            dest = unique_dest_path(inbox_dir, path.name)
            shutil.copy2(path, dest)
            count += 1
    return count  # пользователь видит количество писем для работы

def inbox_is_empty(inbox_dir: Path) -> bool:  # проверка на наличие в inbox обычных (не скрытых) файлов. (цель: не копировать каждый запуск письма, уже лежащие в inbox)
    if not inbox_dir.exists():
        return True
    for path in inbox_dir.iterdir():
        if path.is_file() and not path.name.startswith("."):
            return False
    return True