from core.enum.day_log_type import DayLogType
from logger_factory import LoggerFactory
from model.piyolog_day_record import PiyoLogDayRecord
from model.piyolog_record import PiyoLogRecord
from datetime import date, datetime, timedelta

logger = LoggerFactory.getLogger(__name__)


class PiyologParserAPIData:

    def __init__(self):
        pass

    def parse_record(self, data) -> list[PiyoLogDayRecord]:
        ret: list[PiyoLogDayRecord] = []

        day_log = data["data"]["day_log"]
        baby_event = data["data"]["baby_event"]

        for day_log_data in day_log:
            if day_log_data["deleted"] == True:
                continue

            add_data = PiyoLogDayRecord()

            # 日付
            add_data.date = datetime.strptime(str(day_log_data["date"]), "%Y%m%d")
            logger.debug(str(day_log_data["date"]))

            # 日記
            add_data.daily_memo = day_log_data["diary"]

            # 紐づく日付のデータを取得
            day_records = [
                record
                for record in baby_event
                if (
                    record["date"] == day_log_data["date"]
                    and record["deleted"] == False
                )
            ]

            # 時間でソート
            day_records.sort(key=lambda x: x["time"])

            # レコードを追加
            for record in day_records:
                add_record_data = PiyoLogRecord.from_api(record)
                add_data.records.append(add_record_data)

            # サマリーの割り当て
            add_data.summary.bleast_feed_time_left = sum(
                [
                    record["left_time"]
                    for record in baby_event
                    if (
                        record["date"] == day_log_data["date"]
                        and record["deleted"] == False
                        and record["type"] == 1
                    )
                ]
            )
            add_data.summary.bleast_feed_time_right = sum(
                [
                    record["right_time"]
                    for record in baby_event
                    if (
                        record["date"] == day_log_data["date"]
                        and record["deleted"] == False
                        and record["type"] == 1
                    )
                ]
            )
            add_data.summary.formula_count = len(
                [
                    record
                    for record in baby_event
                    if (
                        record["date"] == day_log_data["date"]
                        and record["deleted"] == False
                        and record["type"] == 2
                    )
                ]
            )
            add_data.summary.formula_total_amount = sum(
                [
                    record["amount"]
                    for record in baby_event
                    if (
                        record["date"] == day_log_data["date"]
                        and record["deleted"] == False
                        and record["type"] == 2
                    )
                ]
            )
            add_data.summary.pee_count = len(
                [
                    record
                    for record in baby_event
                    if (
                        record["date"] == day_log_data["date"]
                        and record["deleted"] == False
                        and record["type"] == 6
                    )
                ]
            )
            add_data.summary.poo_count = len(
                [
                    record
                    for record in baby_event
                    if (
                        record["date"] == day_log_data["date"]
                        and record["deleted"] == False
                        and record["type"] == 7
                    )
                ]
            )

            # 「ねる」「起きる」のレコードを抜き出す
            sleep_records = [
                record
                for record in add_data.records
                if (
                    record.record_type == DayLogType.get_type_name(4)
                    or record.record_type == DayLogType.get_type_name(5)
                )
            ]

            for index, sleep_elem in enumerate(sleep_records):
                if sleep_elem.record_type == DayLogType.get_type_name(5):
                    if index == 0:
                        # 起きるレコードが最初の場合
                        add_data.summary.sleep_duration += (
                            sleep_elem.date - add_data.date
                        )
                    elif index > 0:
                        # 起きるレコード：これより前の「ねる」レコードを取得
                        sleep_start = sleep_records[index - 1]
                        add_data.summary.sleep_duration += (
                            sleep_elem.date - sleep_start.date
                        )

                # 最後のレコードが「ねる」の場合
                if index == len(sleep_records) - 1:
                    if sleep_elem.record_type == DayLogType.get_type_name(4):
                        add_data.summary.sleep_duration += (
                            add_data.date + timedelta(hours=24) - sleep_elem.date
                        )

            ret.append(add_data)

        return ret
