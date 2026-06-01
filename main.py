import sys
import argparse
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
SRC = ROOT_DIR / "src"
# Дополнительная проверка на всякий случай
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mail_system.processor import MailProcessor
from mail_system.storage import (
    copy_inbox_files,
    ensure_mailbox_layout,
    extract_zip,
    inbox_is_empty,
)


def build_parser():
    parser = argparse.ArgumentParser(description="Сортировка входящих писем по категориям")
    parser.add_argument("--mailbox", default="mailbox",
                        help="папка для inbox, категорий и логов")
    parser.add_argument("--source", default="data/inbox/inbox",
                        help="откуда брать письма, если inbox пустой")
    parser.add_argument("--zip", default="", help="путь к zip (необязательно)")
    parser.add_argument("--force", action="store_true",
                        help="очистить inbox и скопировать письма заново")
    return parser


def prepare_inbox(mailbox_root, source_dir, zip_path, force):
    ensure_mailbox_layout(mailbox_root)
    inbox_dir = mailbox_root / "inbox"
    if force and inbox_dir.exists():
        for f in inbox_dir.iterdir():
            if f.is_file():
                f.unlink()

    if zip_path and zip_path.exists():
        extract_zip(zip_path, mailbox_root)
        return

    if inbox_is_empty(inbox_dir):
        copy_inbox_files(source_dir, inbox_dir)