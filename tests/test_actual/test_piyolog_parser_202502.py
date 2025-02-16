from datetime import timedelta
from pathlib import Path

from core.piyolog_parser.piyolog_parser_month import PiyoLogParserMonth


def test_parse_202502_actual_android():
    # Arrange
    test_file = Path("piyolog-data-debug/ぴよログ-2025年2月デバッグ用_android.txt")

    with open(test_file, "r") as f:
        test_str = f.read()

    # Act
    parser = PiyoLogParserMonth()
    month_data = parser.parse_str(test_str)

    # Assert
    assert len(month_data) == 17

    # 2/1
    assert month_data[0].summary.formula_count == 5
    assert month_data[0].summary.formula_total_amount == 880
    assert (
        month_data[0].summary.sleep_duration == timedelta(hours=13, minutes=30).seconds
    )
    assert month_data[0].summary.pee_count == 6
    assert month_data[0].summary.poo_count == 1


def test_parse_202502_actual_ios():
    # Arrange
    test_file = Path("piyolog-data-debug/ぴよログ-2025年2月デバッグ用_ios.txt")

    with open(test_file, "r") as f:
        test_str = f.read()

    # Act
    parser = PiyoLogParserMonth()
    month_data = parser.parse_str(test_str)

    # Assert
    assert len(month_data) == 17

    # 2/1
    assert month_data[0].summary.formula_count == 5
    assert month_data[0].summary.formula_total_amount == 880
    assert (
        month_data[0].summary.sleep_duration == timedelta(hours=13, minutes=30).seconds
    )
    assert month_data[0].summary.pee_count == 6
    assert month_data[0].summary.poo_count == 1
