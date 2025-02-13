import asyncio
from datetime import date
import os
from core.piyolog_parser.piyolog_parser_month import PiyoLogParserMonth
from logger_factory import LoggerFactory
from model.piyolog_day_record import PiyoLogDayRecord
import mysql.connector
from repository.piyolog_repository_base import PiyologRepositoryBase
from repository.piyolog_repository_mysql import PiyologRepositoryMySql  

logger = LoggerFactory.getLogger(__name__)

src_dir = "piyolog_data"


async def main():
    try:
        file_list = []
        for dirpath, dirnames, filenames in os.walk(src_dir):
            for filename in filenames:
                # フルパスで取得する場合：
                file_path = os.path.join(dirpath, filename)
                file_list.append(file_path)

        parser = PiyoLogParserMonth()

        month_data_list:list[PiyoLogDayRecord] = []
        for file in file_list:
            logger.info(f"file: {file}")

            with open(file, "r") as f:
                content = f.read()
                month_data = parser.parse_str(content)
                month_data_list.append(month_data)

        # MySQLに接続
        conn = mysql.connector.connect(
            host="localhost",
            database="piyolog",
            user="docker",
            password="docker"
        )
        conn.autocommit = False

        if conn.is_connected():
            logger.debug("Connected to MySQL database")

            repo:PiyologRepositoryBase = PiyologRepositoryMySql(conn)
            
            # for month_data in month_data_list:
            #     for day_data in month_data:
            #         repo.delete_insert_piyolog(day_data)

            get_date = date(2024,12,10)
            day_data = repo.select_piyolog(get_date)

            logger.debug("selected data: %s",day_data)

        else:
            logger.error("Failed to connect MySQL database")

    except Exception as e:
        logger.error(e,exc_info=True)
    finally:
        conn.close()
        logger.info("MySQL connection is closed")

if __name__ == "__main__":
    asyncio.run(main())
