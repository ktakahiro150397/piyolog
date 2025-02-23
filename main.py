import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv

from core.retriever.retrieve_from_sync import RetrievePiyoLogAPI

load_dotenv()

EXECUTION_INTERVAL = int(os.getenv("EXECUTION_INTERVAL", 60))
ALL_DATA_EXECUTION_INTERVAL = int(
    os.getenv("ALL_DATA_EXECUTION_INTERVAL", 60 * 60 * 12)
)

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient
import googleapiclient.discovery
from core.piyolog_parser.piyolog_parser_month import PiyoLogParserMonth
from logger_factory import LoggerFactory
from model.piyolog_day_record import PiyoLogDayRecord
import mysql.connector
from repository.piyolog_repository_base import PiyologRepositoryBase
from repository.piyolog_repository_mysql import PiyologRepositoryMySql
from googleapiclient.discovery import build
from itertools import groupby

logger = LoggerFactory.getLogger(__name__)


async def main():
    execution_interval_sum = 0
    while True:
        if execution_interval_sum >= ALL_DATA_EXECUTION_INTERVAL:
            # 全データ取得の実行
            logger.info("全データ取得を開始")
            await retrieve_data(is_all_data=True)
            logger.info("全データ取得が完了")
            execution_interval_sum = 0
            await asyncio.sleep(EXECUTION_INTERVAL)
        else:
            # データ取得の実行
            logger.info("データ取得を開始")
            await retrieve_data()
            logger.info("データ取得を完了")
            execution_interval_sum += EXECUTION_INTERVAL
            await asyncio.sleep(EXECUTION_INTERVAL)


async def retrieve_data(is_all_data=False):
    try:
        data: list[PiyoLogDayRecord] = []

        retriver = RetrievePiyoLogAPI()
        if is_all_data:
            data = retriver.retrieve_from_force_sync_to_app_endpoint()
        else:
            data = retriver.retrueve_from_sync_endpoint()

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

            for day_data in data:
                repo.delete_insert_piyolog(day_data)
        else:
            logger.error("Failed to connect MySQL database")

        conn.close()
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        logger.info("Process is finished")


if __name__ == "__main__":
    asyncio.run(main())
