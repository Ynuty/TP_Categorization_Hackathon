import sys
import argparse
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
SRC = ROOT_DIR / "src"

from mail_system.processor import MailProcessor
from mail_system.storage import (
    copy_inbox_files,
    ensure_mailbox_layout,
    extract_zip,
    inbox_is_empty,
)