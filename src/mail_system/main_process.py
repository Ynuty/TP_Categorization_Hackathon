from pathlib import Path

from .classificator import RuleBaseClassificator
from .logging_info import logs_creator
from .models import Category, ProcessingStats
from .parser import EmailParser, ParseError
from .storage_in_mailbox import move_file


class MailProcess:
    def __init__(self, mailbox_root: Path):
        self.mailbox_root = Path(mailbox_root)
        self.inbox_dir = self.mailbox_root / "inbox"
        self.log_path = self.mailbox_root / "processing.log"
        self.stats_path = self.mailbox_root / "stats.txt"
        self.parser = EmailParser()
        self.classifier = RuleBaseClassificator()
        self.logger = logs_creator(self.log_path)


    def run(self) -> ProcessingStats:
        stats = ProcessingStats()

    
        if not self.inbox_dir.exists():
            self._write_stats(stats)
            return stats

        #читаем письма 
        files = [
            p for p in sorted(self.inbox_dir.iterdir())
            if p.is_file() and not p.name.startswith(".")
        ]

        for path in files:
            try:
                email = self.parser.parse(path)
                result = self.classifier.classify(email)
                dest_dir = self.mailbox_root / result.category.value
                move_file(path, dest_dir)
                stats.add(result.category)

                self.logger.info(
                    "%s -> %s | %s",
                    path.name,
                    result.category.value,
                    result.reason,
                )
            
            except ParseError as err:
                dest_dir = self.mailbox_root / Category.FAILED.value
                if path.exists():
                    move_file(path, dest_dir)

                stats.add(Category.FAILED)

                self.logger.error("%s -> failed | %s", path.name, err)

        self._write_stats(stats)
        return stats

    
    def _write_stats(self, stats: ProcessingStats) -> None:
        lines = stats.report_lines()

        self.stats_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        