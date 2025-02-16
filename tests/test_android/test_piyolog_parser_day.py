from datetime import date, timedelta
from core.enum.parser_os_type import ParserOSType
from core.piyolog_parser.piyolog_parser_day import PiyoLogParserDay

UNITTEST_ASSERT_STR = """2024/12/1(日)
あかさん (2か月5日)

01:45   起きる (2時間5分)  
01:50   ミルク 120ml  
02:00   寝る  
04:45   起きる (2時間45分)  
04:50   ミルク 140ml  
21:20   寝る  寝かしつけ終わったぁあああああああああああああああああああああああああああああああああああああ＼(^^)／

ご飯温めよったら、起きたああああああ
13:40   うんち (多め/やわらかめ/緑)  大うんこ💩2日分一気に出てよかった。
手にうんこつけるのはやめてぇ。ロタ打ったあとなので、洗面台で手洗いしました。
14:20   寝る  

母乳合計 左 5分 / 右 6分
ミルク合計 7回 860ml
睡眠合計 12時間5分
おしっこ合計 2回
うんち合計 1回

E赤ちゃんにしてから、ミルクの吐き戻しが少なくなった気がする。

"""


def test_parse_record_date():
    # Arrange
    parser = PiyoLogParserDay(os=ParserOSType.android)

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR)

    # Assert
    assert record.date == date(2024, 12, 1)


def test_parse_record_count():
    # Arrange
    parser = PiyoLogParserDay(os=ParserOSType.android)

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR)

    # Assert
    assert len(record.records) == 8


def test_parse_record_daily_memo():
    # Arrange
    parser = PiyoLogParserDay(os=ParserOSType.android)

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR)

    # Assert
    assert (
        record.daily_memo
        == "E赤ちゃんにしてから、ミルクの吐き戻しが少なくなった気がする。"
    )


def test_parse_record_summary_bleast_feed_time_left():
    # Arrange
    parser = PiyoLogParserDay(os=ParserOSType.android)

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR)

    # Assert
    assert record.summary.bleast_feed_time_left == 5


def test_parse_record_summary_bleast_feed_time_right():
    # Arrange
    parser = PiyoLogParserDay(os=ParserOSType.android)

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR)

    # Assert
    assert record.summary.bleast_feed_time_right == 6


def test_parse_record_summary_formula_count():
    # Arrange
    parser = PiyoLogParserDay(os=ParserOSType.android)

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR)

    # Assert
    assert record.summary.formula_count == 7


def test_parse_record_summary_formula_formula_total_amount():
    # Arrange
    parser = PiyoLogParserDay(os=ParserOSType.android)

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR)

    # Assert
    assert record.summary.formula_total_amount == 860


def test_parse_record_summary_formula_formula_total_amount():
    # Arrange
    parser = PiyoLogParserDay(os=ParserOSType.android)

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR)

    # Assert
    assert record.summary.sleep_duration == timedelta(hours=12, minutes=5)


def test_parse_record_summary_pee_count():
    # Arrange
    parser = PiyoLogParserDay(os=ParserOSType.android)

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR)

    # Assert
    assert record.summary.pee_count == 2


def test_parse_record_summary_poo_count():
    # Arrange
    parser = PiyoLogParserDay(os=ParserOSType.android)

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR)

    # Assert
    assert record.summary.poo_count == 1
