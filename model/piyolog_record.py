from dataclasses import dataclass
from datetime import datetime
from typing import Any

from core.enum.day_log_type import DayLogType


@dataclass
class PiyoLogRecord:
    """ぴよログで入力された単一のレコード"""

    date: datetime
    """データ日付"""

    record_type: str
    """記録の種類"""

    additional_record_data: str
    """存在する場合、記録の追加情報。存在しない場合はNone"""

    record_memo: str
    """記録メモ"""

    def __init__(self):
        self.date = None
        self.record_type = ""
        self.additional_record_data = ""
        self.record_memo = ""

    def insert_param_tuple(self):
        return (
            self.date,
            self.record_type,
            self.additional_record_data,
            self.record_memo,
        )

    @classmethod
    def from_api(cls, api_data: dict):
        rec = cls()

        rec.date = datetime.strptime(api_data["datetime"], "%Y%m%d %H:%M")
        rec.record_type = DayLogType.get_type_name(api_data["type"])
        rec.record_memo = api_data["memo"]
        rec.additional_record_data = DayLogType.get_type_additional_memo(api_data)

        return rec
