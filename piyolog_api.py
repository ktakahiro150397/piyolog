import asyncio
import itertools
import json
import mysql
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from core.piyolog_parser.piyolog_parser_api_data import PiyologParserAPIData
from core.retriever.retrieve_from_sync import RetrievePiyoLogAPI
from logger_factory import LoggerFactory
from functools import reduce
import mysql.connector

from repository.piyolog_repository_base import PiyologRepositoryBase
from repository.piyolog_repository_mysql import PiyologRepositoryMySql

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

    retriver = RetrievePiyoLogAPI()
    sync_endpoint = retriver.retrueve_from_sync_endpoint()
    force_sync_to_app_endpoint = retriver.retrieve_from_force_sync_to_app_endpoint()

    logger.debug(sync_endpoint)
    logger.debug(force_sync_to_app_endpoint)

    logger.info("piyolog api access end")

    # POSTリクエスト
    # response = requests.post(url, headers=headers, json=payload)

    # with open("docs/response.json", "w") as f:
    #     f.write(response.text)

    # logger.debug(response.json())

    # # ローカルファイルから読み込む
    # with open("docs/force_sync_to_app.json", "r") as f:
    #     response = f.read()

    # response = json.loads(response)

    # parser = PiyologParserAPIData()
    # data_list = parser.parse_record(response)

    # logger.debug(data_list)

    # # MySQLに接続
    # conn = mysql.connector.connect(
    #     host=os.getenv("PIYOLOG_DATA_DB_HOST"),
    #     database=os.getenv("PIYOLOG_DATA_DB_DATABASE"),
    #     user=os.getenv("PIYOLOG_DATA_DB_USER"),
    #     password=os.getenv("PIYOLOG_DATA_DB_PASSWORD"),
    # )
    # conn.autocommit = False

    # if conn.is_connected():
    #     logger.debug("Connected to MySQL database")

    #     repo: PiyologRepositoryBase = PiyologRepositoryMySql(conn)

    #     for day_data in data_list:
    #         repo.delete_insert_piyolog(day_data)


if __name__ == "__main__":
    asyncio.run(main())
