from datetime import date
from model.piyolog_day_record import PiyoLogDayRecord
from model.piyolog_record import PiyoLogRecord


class PiyoLogParserBase:
    """ぴよログファイルパーサーの基底クラス"""

    def __init__(self):
        pass

    def parse_file(self, file_path: str) -> list[PiyoLogDayRecord]:
        # Implement this method in the subclass
        raise NotImplementedError()

    def parse_record_line(self, base_date: date, line: str) -> PiyoLogRecord:
        # Implement this method in the subclass
        raise NotImplementedError()
