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

    # retriver = RetrievePiyoLogAPI()
    # sync_endpoint = retriver.retrueve_from_sync_endpoint()
    # force_sync_to_app_endpoint = retriver.retrieve_from_force_sync_to_app_endpoint()

    # logger.debug(sync_endpoint)
    # logger.debug(force_sync_to_app_endpoint)

    # logger.info("piyolog api access end")

    # POSTリクエスト
    # response = requests.post(url, headers=headers, json=payload)

    # with open("docs/response.json", "w") as f:
    #     f.write(response.text)

    # logger.debug(response.json())

    # ローカルファイルから読み込む
    with open("docs/force_sync_to_app.json", "r") as f:
        response = f.read()

    response = json.loads(response)

    # # 20241201のみに絞る
    # date_filterd = [x for x in response["data"]["baby_event"] if x["date"] == 20241215]
    # logger.debug(date_filterd)

    parser = PiyologParserAPIData()
    data_list = parser.parse_record(response)

    logger.debug(data_list)

    # MySQLに接続
    conn = mysql.connector.connect(
        host=os.getenv("PIYOLOG_DATA_DB_HOST"),
        database=os.getenv("PIYOLOG_DATA_DB_DATABASE"),
        user=os.getenv("PIYOLOG_DATA_DB_USER"),
        password=os.getenv("PIYOLOG_DATA_DB_PASSWORD"),
    )
    conn.autocommit = False

    if conn.is_connected():
        logger.debug("Connected to MySQL database")

        repo: PiyologRepositoryBase = PiyologRepositoryMySql(conn)

        for day_data in data_list:
            repo.delete_insert_piyolog(day_data)


if __name__ == "__main__":
    asyncio.run(main())
