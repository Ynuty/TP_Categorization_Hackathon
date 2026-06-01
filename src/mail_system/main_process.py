from pathlib import Path

from .classificator import RuleBaseClassificator
from .logging_info import logs_creator
from .models import Category, ProcessingStats
from .parser import EmailParser, ParseError
from .storage_in_mailbox import move_file


class MainProcess:
    def __init__(self):
        self.inbox_dir = Path("inbox/inbox")
        self.outputroot = Path("data")
        self.log_path = self.output_root / "processing.log"
        self.stats_path = self.output_root / "stats.txt"
        self.parser = EmailParser()
        self.classificator = RuleBaseClassificator()
        self.logger = setup_logger(self.log_path)
        self._init_folders()

    def _init_folders(self):
        self.output_root.mkdir(parents=True, exist_ok=True)

        for category in Category:
            (self.output_root / category.value).mkdir(exist_ok=True)



    
