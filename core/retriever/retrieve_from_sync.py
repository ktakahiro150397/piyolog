import os

import requests

from core.piyolog_parser.piyolog_parser_api_data import PiyologParserAPIData
from logger_factory import LoggerFactory
from model.piyolog_day_record import PiyoLogDayRecord

ENDPOINT_SYNC_URL = "https://api2.piyolog.com/sync"
ENDPOINT_FORCE_SYNC_TO_APP_URL = "https://api2.piyolog.com/force_sync_to_app"

logger = LoggerFactory.getLogger(__name__)


class RetrievePiyoLogAPI:
    def __init__(self):
        self.piyolog_api_user_id = os.getenv("PIYOLOG_API_USER_ID")
        self.piyolog_api_client_token = os.getenv("PIYOLOG_API_CLIENT_TOKEN")

    def retrueve_from_sync_endpoint(self) -> list[PiyoLogDayRecord]:
        return self._retrieve_from_endpoint(ENDPOINT_SYNC_URL)

    def retrieve_from_force_sync_to_app_endpoint(self) -> list[PiyoLogDayRecord]:
        return self._retrieve_from_endpoint(ENDPOINT_FORCE_SYNC_TO_APP_URL)

    def _retrieve_from_endpoint(self, url: str) -> list[PiyoLogDayRecord]:
        logger.info(f"{url} からデータを取得します。")

        try:
            headers = self._get_header()
            payload = self._get_payload()

            # POSTリクエスト
            response = requests.post(url, headers=headers, json=payload)

            response.raise_for_status()
            response_json = response.json()

            parser = PiyologParserAPIData()
            data_list = parser.parse_record(response_json)

            return data_list
        except Exception as e:
            logger.error(f"APIリクエストに失敗しました。: {e}")
            return []

    def _get_header(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "PiyoLog/505 CFNetwork/1568.200.51 Darwin/24.1.0",
            "Accept-Language": "ja",
            "Accept-Encoding": "gzip, deflate, br",
        }

    def _get_payload(self):
        return {
            "client_token": self.piyolog_api_client_token,
            "app": "PiyoLog for iPhone",
            "api_version": 2.1000000000000001,
            "minor_version": 6808,
            "user_id": self.piyolog_api_user_id,
            "main_version": 1,
            "client_id": 2,
        }
