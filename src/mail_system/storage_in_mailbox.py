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

def move_file(src: Path, dest_dir: Path) -> Path:  # перемещает текущий файл в папку категории из inbox
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = unique_dest_path(dest_dir, src.name)  # изначатльно ставим файлу безопасное (unique) имя
    shutil.move(str(src), str(dest))
    return dest


def extract_zip(zip_path: Path, target_dir: Path) -> None:  # распапковка zip с письмами
    target_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(target_dir)

def copy_inbox_files(source_dir: Path, inbox_dir: Path) -> int:  # копирует массив писем из источника в inbox
    inbox_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(source_dir.iterdir()):
        if path.is_file() and not path.name.startswith("."):  # благодаря .startswith() пропускаем скрытые файлы
            dest = unique_dest_path(inbox_dir, path.name)
            shutil.copy2(path, dest)
            count += 1
    return count  # пользователь видит количество писем для работы