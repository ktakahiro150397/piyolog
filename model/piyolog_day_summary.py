from dataclasses import dataclass
from datetime import timedelta


@dataclass
class PiyoLogDaySummary:
    """ぴよログで入力された1日の記録のサマリー"""

    bleast_feed_time_left: int
    """左授乳時間"""

    bleast_feed_time_right: int
    """右授乳時間"""

    formula_count: int
    """ミルク回数"""

    formula_total_amount: int
    """ミルク合計量"""

    sleep_duration: timedelta
    """睡眠時間合計"""

    pee_count: int
    """おしっこ回数合計"""

    poo_count: int
    """うんち回数合計"""

    def __init__(self):
        self.bleast_feed_time_left = 0
        self.bleast_feed_time_right = 0
        self.formula_count = 0
        self.formula_total_amount = 0
        self.sleep_duration = timedelta()
        self.pee_count = 0
        self.poo_count = 0

    def insert_param_tuple(self):
        return (
            self.bleast_feed_time_left,
            self.bleast_feed_time_right,
            self.formula_count,
            self.formula_total_amount,
            self.sleep_duration.seconds,
            self.pee_count,
            self.poo_count
        )
