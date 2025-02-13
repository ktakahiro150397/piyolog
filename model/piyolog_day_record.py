from dataclasses import dataclass
from sqlite3 import Date
from typing import Tuple
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

    def insert_param_tuple(self) -> Tuple[Date, str]:
        return (self.date, self.daily_memo)

    def from_tuple(self, data: Tuple):
        self.date = data[0]
        self.daily_memo = data[1]

    @classmethod
    def from_dict(cls,data:dict) -> 'PiyoLogDayRecord':
        valid_keys = cls.__dataclass_fields__.keys()
        filtered = {key: value for key,value in data.items() if key in valid_keys}  
        
        ret = PiyoLogDayRecord()
        ret.date = filtered["date"]
        ret.daily_memo = filtered["daily_memo"]
        
        return ret
