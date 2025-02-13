from datetime import date, datetime
from core.consts.piyolog_parser_consts import PIYOLOG_EXPORT_FILE_DELIMITER
from model.piyolog_day_record import PiyoLogDayRecord
from model.piyolog_record import PiyoLogRecord


class PiyoLogParserBase:
    """ぴよログファイルパーサーの基底クラス"""

    def __init__(self):
        pass

    def parse_record_line(self, base_date: date, line: str) -> PiyoLogRecord:
        # Split line by 3 spaces
        line_parts = line.split(PIYOLOG_EXPORT_FILE_DELIMITER)

        if len(line_parts) == 2 :
            line_parts.append("")

        if len(line_parts) != 3:
            raise ValueError(f"Invalid line format: {line}")

        ret = PiyoLogRecord()

        # Extract and format time : "HH:mm"
        time_str = line_parts[0]
        time_parts = time_str.split(":")
        if len(time_parts) != 2:
            raise ValueError(f"Invalid time format: {time_str}")

        ret.date = datetime(
            base_date.year,
            base_date.month,
            base_date.day,
            int(time_parts[0]),
            int(time_parts[1]),
        )

        # Extract record type
        ret.record_type = line_parts[1]
        # Split record type and additional data
        type_parts = ret.record_type.split(" ")
        ret.record_type = type_parts[0]
        if len(type_parts) > 1:
            ret.additional_record_data = type_parts[1].replace("(", "").replace(")", "")

        # Extract memo
        ret.record_memo = line_parts[2].strip("\n")

        return ret
