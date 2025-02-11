from dataclasses import dataclass
from sqlite3 import Date
from model.piyolog_day_summary import PiyoLogDaySummary
from model.piyolog_record import PiyoLogRecord


@dataclass
class PiyoLogDayRecord:
    """ぴよログで入力された1日のレコード"""

    date: Date
    """日付"""

    birthDayCount: int
    """生まれてからの日数"""

    records: list[PiyoLogRecord]
    """記録のリスト"""

    daily_memo: str
    """記録メモ"""

    summary: PiyoLogDaySummary
    """1日のサマリー"""
