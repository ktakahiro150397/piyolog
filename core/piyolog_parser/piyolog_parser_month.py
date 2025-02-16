from datetime import date, datetime, timedelta
import re
from core.enum.parser_os_type import ParserOSType
from core.piyolog_parser.piyolog_parser_base import PiyoLogParserBase
from core.piyolog_parser.piyolog_parser_day import PiyoLogParserDay
from model.piyolog_day_record import PiyoLogDayRecord
from model.piyolog_day_summary import PiyoLogDaySummary


class PiyoLogParserMonth(PiyoLogParserBase):
    """ぴよログファイルパーサー(月毎)"""

    def __init__(self, os: ParserOSType = ParserOSType.ios):
        super().__init__(os=os)

    def parse_str(self, input_str: str) -> list[PiyoLogDayRecord]:
        # OSの判別
        if input_str.startswith("ぴよログ"):
            self.os = ParserOSType.android

        record_str_list = input_str.split("----------")

        pattern = r"^\n\d{4}/\d{1,2}/\d{1,2}"
        record_str_list = [
            record_str
            for record_str in record_str_list
            if (record_str.strip() and re.match(pattern, record_str))
        ]

        day_parser = PiyoLogParserDay(self.os)
        ret = [day_parser.parse_str(record_str) for record_str in record_str_list]

        return ret
