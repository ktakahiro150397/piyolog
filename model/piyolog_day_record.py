from dataclasses import dataclass
from sqlite3 import Date
from model.piyolog_day_summary import PiyoLogDaySummary
from model.piyolog_record import PiyoLogRecord


@dataclass
class PiyoLogDayRecord:
    """ぴよログで入力された1日のレコード"""

    date: Date
    """日付"""

    records: list[PiyoLogRecord]
    """記録のリスト"""

    daily_memo: str
    """記録メモ"""

    summary: PiyoLogDaySummary
    """1日のサマリー"""

    def __init__(self):
        self.date = None
        self.records = []
        self.daily_memo = ""
        self.summary = PiyoLogDaySummary()
        pass
