from datetime import date, datetime
from core.consts.piyolog_parser_consts import (
    PIYOLOG_EXPORT_FILE_DELIMITER,
    PIYOLOG_EXPORT_FILE_ANDROID_MEMO_DELIMITER,
)
from core.enum.parser_os_type import ParserOSType
from model.piyolog_day_record import PiyoLogDayRecord
from model.piyolog_record import PiyoLogRecord


class PiyoLogParserBase:
    """ぴよログファイルパーサーの基底クラス"""

    def __init__(self, os: ParserOSType = ParserOSType.ios):
        self.os = os

    def parse_record_line(self, base_date: date, line: str) -> PiyoLogRecord:
        if self.os == ParserOSType.ios:
            return self._parse_record_line_ios(base_date, line)
        elif self.os == ParserOSType.android:
            return self._parse_record_line_android(base_date, line)
        else:
            raise ValueError(f"Invalid OS type: {self.os}")

    def _parse_record_line_ios(self, base_date: date, line: str) -> PiyoLogRecord:
        """iOS出力ファイルの行データをパースします。"""

        # Split line by 3 spaces
        line_parts = line.split(PIYOLOG_EXPORT_FILE_DELIMITER)

        if len(line_parts) == 2:
            line_parts.append("")

        if len(line_parts) > 3:
            # インデックス2以降はPIYOLOG_EXPORT_FILE_DELIMITERで再結合する
            # メモ中にデリミタが含まれている
            line_parts[2] = PIYOLOG_EXPORT_FILE_DELIMITER.join(line_parts[2:])
            del line_parts[3:]

        if len(line_parts) != 3:
            raise ValueError(f"Invalid line format: {line}")

        return self._parse_record_line(base_date, line_parts)

    def _parse_record_line_android(self, base_date: date, line: str) -> PiyoLogRecord:
        """Android出力ファイルの行データをパースします。"""

        # Split line by 3 spaces
        line_parts = line.split(PIYOLOG_EXPORT_FILE_DELIMITER)

        # 2つ目以降の要素をさらにAndroidのデリミタで分割
        if len(line_parts) > 1:
            line_parts[1:] = line_parts[1].split(
                PIYOLOG_EXPORT_FILE_ANDROID_MEMO_DELIMITER
            )

        return self._parse_record_line(base_date, line_parts)

    def _parse_record_line(self, base_date: date, line_parts: list[str]):
        """入力ごとに区切られた行データをパースします。"""

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
