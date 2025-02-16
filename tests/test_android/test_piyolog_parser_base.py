from datetime import date, datetime
from core.piyolog_parser.piyolog_parser_base import PiyoLogParserBase

UNITTEST_BASE_DATE = date(2024, 12, 1)


def test_parse_line_wakeup():
    """起きる記録の行をパースする"""

    # Arrange
    test_line = "01:45   起きる (2時間5分)  "
    parser = PiyoLogParserBase()

    # Act
    record = parser.parse_record_line(UNITTEST_BASE_DATE, test_line)

    # Assert
    assert record.date == datetime(2024, 12, 1, 1, 45)
    assert record.record_type == "起きる"
    assert record.additional_record_data == "2時間5分"
    assert record.record_memo == ""


def test_parse_line_formula():
    """ミルク記録の行をパースする"""

    # Arrange
    test_line = "01:50   ミルク 120ml  "
    parser = PiyoLogParserBase()

    # Act
    record = parser.parse_record_line(UNITTEST_BASE_DATE, test_line)

    # Assert
    assert record.date == datetime(2024, 12, 1, 1, 50, 0)
    assert record.record_type == "ミルク"
    assert record.additional_record_data == "120ml"
    assert record.record_memo == ""


def test_parse_line_sleep():
    """寝る記録の行をパースする"""

    # Arrange
    test_line = "02:00   寝る  "
    parser = PiyoLogParserBase()

    # Act
    record = parser.parse_record_line(UNITTEST_BASE_DATE, test_line)

    # Assert
    assert record.date == datetime(2024, 12, 1, 2, 0, 0)
    assert record.record_type == "寝る"
    assert record.additional_record_data == ""
    assert record.record_memo == ""


def test_parse_line_memo():
    """メモ記録の行をパースする"""

    # Arrange
    test_line = "13:00   メモ  ぐずぐず。抱っこしたかな泣く。重すぎる。"
    parser = PiyoLogParserBase()

    # Act
    record = parser.parse_record_line(UNITTEST_BASE_DATE, test_line)

    # Assert
    assert record.date == datetime(2024, 12, 1, 13, 0, 0)
    assert record.record_type == "メモ"
    assert record.additional_record_data == ""
    assert record.record_memo == "ぐずぐず。抱っこしたかな泣く。重すぎる。"


def test_parse_line_temperature():
    """体温記録の行をパースする"""

    # Arrange
    test_line = "13:55   体温 36.6°C  "
    parser = PiyoLogParserBase()

    # Act
    record = parser.parse_record_line(UNITTEST_BASE_DATE, test_line)

    # Assert
    assert record.date == datetime(2024, 12, 1, 13, 55, 0)
    assert record.record_type == "体温"
    assert record.additional_record_data == "36.6°C"
    assert record.record_memo == ""
