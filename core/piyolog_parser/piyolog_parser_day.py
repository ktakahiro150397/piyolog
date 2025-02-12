from datetime import date, datetime, timedelta
import re
from core.piyolog_parser.piyolog_parser_base import PiyoLogParserBase
from model.piyolog_day_record import PiyoLogDayRecord
from model.piyolog_day_summary import PiyoLogDaySummary


class PiyoLogParserDay(PiyoLogParserBase):
    """ぴよログファイルパーサー(日毎)"""

    def __init__(self):
        super().__init__()

    def parse_str(self, input_str: str) -> PiyoLogDayRecord:
        # 日付、レコード、サマリー、メモの順で分割
        ret = PiyoLogDayRecord()

        # 改行で分割
        lines = input_str.split("\n\n")

        # 日付は最初の2行
        date_part = lines[0]
        match = re.search(r"^(\d{4}/\d{1,2}/\d{1,2})", date_part)
        if match:
            date_str = match.group(1)
            ret.date = datetime.strptime(date_str, "%Y/%m/%d").date()

        # 「母乳合計」で始まる行の手前までがレコード
        record_part_end = 1
        record_part = ""
        for line in lines[1:]:
            if line.startswith("母乳合計"):
                break
            record_part += line + "\n"
            record_part_end += 1
        ret.records = self._parse_record_part(ret.date, record_part)

        # 「母乳合計」で始まる行がサマリー
        summary_part = lines[record_part_end]
        ret.summary = self._parse_summary(summary_part)

        # 残りがメモ
        memo_part = lines[record_part_end + 1]
        ret.daily_memo = memo_part

        return ret

    def _parse_summary(self, summary_part: str) -> PiyoLogDaySummary:
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

    def _parse_record_part(
        self, base_date: date, record_part: str
    ) -> list[PiyoLogDayRecord]:
        # %d%d:%d%d で文字列を分割
        reEx = r"(?=\d{2}:\d{2})"

        records = re.split(reEx, record_part)
        # TODO : 2024/12/15 メモ中の時刻表記に対応する
        ret = [
            self.parse_record_line(base_date, record)
            for record in records
            if record.strip()
        ]

        return ret
