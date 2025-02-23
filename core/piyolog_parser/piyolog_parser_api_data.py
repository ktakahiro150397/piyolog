from model.piyolog_day_record import PiyoLogDayRecord
from model.piyolog_record import PiyoLogRecord
from datetime import date, datetime


class PiyologParserAPIData:

    def __init__(self):
        pass

    def parse_record(self, data) -> list[PiyoLogDayRecord]:
        ret: list[PiyoLogDayRecord] = []

        day_log = data["data"]["day_log"]
        baby_event = data["data"]["baby_event"]

        for day_log_data in day_log:
            add_data = PiyoLogDayRecord()

            # 日付
            add_data.date = datetime.strptime(str(day_log_data["date"]), "%Y%m%d")

            # 日記
            add_data.daily_memo = day_log_data["diary"]

            # 紐づく日付のデータを取得
            day_records = [
                record
                for record in baby_event
                if record["date"] == day_log_data["date"]
            ]

            # 時間でソート
            day_records.sort(key=lambda x: x["time"])

            # レコードを追加
            for record in day_records:
                add_record = PiyoLogRecord.from_api(record)
                add_data.records.append(add_record)

            ret.append(add_data)

        return ret
