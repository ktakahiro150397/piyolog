from datetime import date, datetime, timedelta
from io import StringIO
import re
from core.consts.piyolog_parser_consts import PIYOLOG_EXPORT_FILE_DELIMITER
from core.enum.parser_os_type import ParserOSType
from core.piyolog_parser.piyolog_parser_base import PiyoLogParserBase
from model.piyolog_day_record import PiyoLogDayRecord
from model.piyolog_day_summary import PiyoLogDaySummary


class PiyoLogParserDay(PiyoLogParserBase):
    """ぴよログファイルパーサー(日毎)"""

    def __init__(self, os: ParserOSType = ParserOSType.ios):
        super().__init__(os=os)

    def parse_str(self, input_str: str) -> PiyoLogDayRecord:
        # 日付、レコード、サマリー、メモの順で分割
        ret = PiyoLogDayRecord()

        # 改行で分割
        lines = input_str.split("\n")

        # 日付はyyyy/mm/dd形式にマッチする行+次の1行
        record_part_end = 0
        is_parse_end = False
        for i, line in enumerate(lines):
            match = re.search(r"^(\d{4}/\d{1,2}/\d{1,2})", line)
            if not is_parse_end and match:
                date_str = match.group(1)
                ret.date = datetime.strptime(date_str, "%Y/%m/%d").date()
                is_parse_end = True

            if is_parse_end and line == "":
                record_part_end = i
                break

        # 「母乳合計」で始まる行の手前までがレコード
        record_part = ""
        for line in lines[(record_part_end + 1) :]:
            if line.startswith("母乳合計"):
                break
            record_part += line + "\n"
            record_part_end += 1
        ret.records = self._parse_record_part(ret.date, record_part)

        # 「母乳合計」で始まり、「うんち合計」で終わる行がサマリー
        summary_part = ""
        for line in lines[(record_part_end + 1) :]:
            if line == "":
                summary_part = summary_part.strip("\n")
                break
            else:
                summary_part += line + "\n"
            record_part_end += 1

        ret.summary = self._parse_summary(summary_part)

        if len(lines) <= record_part_end + 2:
            # 日レコードのメモなし
            ret.daily_memo = ""
            return ret
        else:
            # 残りがメモ
            memo_part = "\n".join(lines[(record_part_end + 2) : len(lines) - 2])
            ret.daily_memo = memo_part

            return ret

    def _parse_summary(self, summary_part: str) -> PiyoLogDaySummary:
        if self.os == ParserOSType.ios:
            return self._parse_summary_ios(summary_part)
        elif self.os == ParserOSType.android:
            return self._parse_summary_android(summary_part)
        else:
            raise ValueError(f"Invalid OS type: {self.os}")

    def _parse_summary_ios(self, summary_part: str) -> PiyoLogDaySummary:
        ret = PiyoLogDaySummary()

        summary_lines = summary_part.split("\n")

        # 母乳合計
        match = re.search(r"母乳合計　　   左 (\d+)分 / 右 (\d+)分", summary_lines[0])
        if match:
            ret.bleast_feed_time_left = int(match.group(1))
            ret.bleast_feed_time_right = int(match.group(2))

        # ミルク合計
        match = re.search(r"ミルク合計　   (\d+)回 (\d+)ml", summary_lines[1])
        if match:
            ret.formula_count = int(match.group(1))
            ret.formula_total_amount = int(match.group(2))

        # 睡眠時間
        match = re.search(r"睡眠合計　　   (\d+)時間(\d+)分", summary_lines[2])
        if match:
            ret.sleep_duration = timedelta(
                hours=int(match.group(1)), minutes=int(match.group(2))
            )

        # おしっこ
        match = re.search(r"おしっこ合計   (\d+)回", summary_lines[3])
        if match:
            ret.pee_count = int(match.group(1))

        # うんち
        match = re.search(r"うんち合計　   (\d+)回", summary_lines[4])
        if match:
            ret.poo_count = int(match.group(1))

        return ret

    def _parse_summary_android(self, summary_part: str) -> PiyoLogDaySummary:
        ret = PiyoLogDaySummary()

        summary_lines = summary_part.split("\n")

        # 母乳合計
        match = re.search(r"母乳合計 左 (\d+)分 / 右 (\d+)分", summary_lines[0])
        if match:
            ret.bleast_feed_time_left = int(match.group(1))
            ret.bleast_feed_time_right = int(match.group(2))

        # ミルク合計
        match = re.search(r"ミルク合計 (\d+)回 (\d+)ml", summary_lines[1])
        if match:
            ret.formula_count = int(match.group(1))
            ret.formula_total_amount = int(match.group(2))

        # 睡眠時間
        match = re.search(r"睡眠合計 (\d+)時間(\d+)分", summary_lines[2])
        if match:
            ret.sleep_duration = timedelta(
                hours=int(match.group(1)), minutes=int(match.group(2))
            )

        # おしっこ
        match = re.search(r"おしっこ合計 (\d+)回", summary_lines[3])
        if match:
            ret.pee_count = int(match.group(1))

        # うんち
        match = re.search(r"うんち合計 (\d+)回", summary_lines[4])
        if match:
            ret.poo_count = int(match.group(1))

        return ret

    def _parse_record_part(
        self, base_date: date, record_part: str
    ) -> list[PiyoLogDayRecord]:
        # まさか、自力でエスケープを!?
        # 0 スペースを$に変換
        record_part = record_part.replace(PIYOLOG_EXPORT_FILE_DELIMITER, "$")

        # 1 スペースをダブルクォートで囲む
        record_part = record_part.replace("$", '"$"')

        # 2 行ごとに、\d{2}:\d{2}で始まっている場合は文頭にクォートを付与
        timeEx = r"^(\d{2}:\d{2}).*\$.*"
        record_lines = [line for line in record_part.split("\n")]
        for i, line in enumerate(record_lines):
            if re.match(timeEx, line):
                # 行ごとに、\d{2}:\d{2}で始まっている場合は文頭にクォートを付与
                record_lines[i] = '"' + record_lines[i]

                if line.endswith('"$"'):
                    # 末尾が"$"の場合、クォートをさらに末尾に付与
                    record_lines[i] = record_lines[i] + '"'
                else:
                    # 次の行が存在し、\d{2}:\d{2}で始まっている場合はクォートを末尾に付与
                    if i + 1 < len(record_lines) and re.match(
                        timeEx, record_lines[i + 1]
                    ):
                        record_lines[i] = record_lines[i] + '"'
                    else:
                        # それ以外の場合、改行を末尾に付与
                        record_lines[i] = record_lines[i] + "\n"
            else:
                # 次の行が存在し、\d{2}:\d{2}で始まっている場合はクォートを末尾に付与
                if i + 1 < len(record_lines) and re.match(timeEx, record_lines[i + 1]):
                    record_lines[i] = record_lines[i] + '"'
                else:
                    # それ以外の場合、改行を末尾に付与
                    record_lines[i] = record_lines[i] + "\n"

        # 3 csvReaderでパースするために文字列に戻す
        record_csv_str = ""
        for i, line in enumerate(record_lines):
            if i != (len(record_lines) - 1) and line.endswith('"'):
                record_csv_str += line + "\n"
            else:
                record_csv_str += line

        import csv

        parsed_list = [
            row for row in csv.reader(StringIO(record_csv_str), delimiter="$")
        ]

        records = [PIYOLOG_EXPORT_FILE_DELIMITER.join(row) for row in parsed_list]

        ret = [
            self.parse_record_line(base_date, record)
            for record in records
            if record.strip()
        ]

        return ret
