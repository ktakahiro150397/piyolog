from dataclasses import dataclass
from datetime import datetime
from typing import Any


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
