from datetime import timedelta
import json
import os
from core.piyolog_parser.piyolog_parser_api_data import PiyologParserAPIData


def test_sleep_duration_initial_sleep():
    # Arrange
    with open(
        "tests/test_api/test_response/test_sleep_duration_initial_sleep.json", "r"
    ) as f:
        test_data_str = f.read()

    test_data = json.loads(test_data_str)
    parser = PiyologParserAPIData()

    # Act
    result = parser.parse_record(test_data)

    # Assert
    assert result[0].summary.sleep_duration == timedelta(hours=12, minutes=5)


def test_sleep_duration_initial_wakeup():
    # Arrange
    with open(
        "tests/test_api/test_response/test_sleep_duration_initial_wakeup.json", "r"
    ) as f:
        test_data_str = f.read()

    test_data = json.loads(test_data_str)
    parser = PiyologParserAPIData()

    # Act
    result = parser.parse_record(test_data)

    # Assert
    assert result[0].summary.sleep_duration == timedelta(hours=9, minutes=50)
