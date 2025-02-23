import asyncio
import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from core.piyolog_parser.piyolog_parser_api_data import PiyologParserAPIData
from logger_factory import LoggerFactory

load_dotenv()

logger = LoggerFactory.getLogger(__name__)

user_id = os.getenv("PIYOLOG_API_USER_ID")
client_token = os.getenv("PIYOLOG_API_CLIENT_TOKEN")


async def main():
    logger.info("piyolog api access")

    # /syncを呼び出す
    url = "https://api2.piyolog.com/sync"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "PiyoLog/505 CFNetwork/1568.200.51 Darwin/24.1.0",
        "Accept-Language": "ja",
        "Accept-Encoding": "gzip, deflate, br",
    }

    payload = {
        "client_token": client_token,
        "app": "PiyoLog for iPhone",
        "api_version": 2.1000000000000001,
        "minor_version": 6808,
        "user_id": user_id,
        "main_version": 1,
        "client_id": 2,
    }

    # POSTリクエスト
    # response = requests.post(url, headers=headers, json=payload)

    # with open("docs/response.json", "w") as f:
    #     f.write(response.text)

    # logger.debug(response.json())

    # ローカルファイルから読み込む
    with open("docs/response.json", "r") as f:
        response = f.read()

    response = json.loads(response)

    parser = PiyologParserAPIData()
    data = parser.parse_record(response)

    logger.debug(data)


if __name__ == "__main__":
    asyncio.run(main())
