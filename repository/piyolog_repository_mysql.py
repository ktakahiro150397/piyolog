
from datetime import date
from logger_factory import LoggerFactory
from model.piyolog_day_record import PiyoLogDayRecord
from repository.mysql_query import insert_queries,delete_queries,select_queries
from repository.piyolog_repository_base import PiyologRepositoryBase

logger = LoggerFactory.getLogger(__name__)

class PiyologRepositoryMySql(PiyologRepositoryBase):
    def __init__(self,conn ):
        self.conn = conn

    def delete_insert_piyolog(self, data: PiyoLogDayRecord) -> int:
        try:
            cursor = self.conn.cursor()

            # データが存在する場合、削除
            header_id = self.select_piyolog_id(data.date)
            if header_id is not None:
                cursor.execute(delete_queries.DAY_RECORD_SUMMARY_DELETE_SQL, (header_id,))
                cursor.execute(delete_queries.RECOREDS_DELETE_SQL, (header_id,))
                cursor.execute(delete_queries.DAY_RECORD_DELETE_SQL, (header_id,))
                logger.debug("Data deleted: %s", header_id)

            # ヘッダーのインサート
            params = data.insert_param_tuple()
            cursor.execute(insert_queries.DAY_RECORD_INSERT_SQL, params)
            inserted_id = cursor.lastrowid

            # サマリーのインサート
            params = data.summary.insert_param_tuple()
            cursor.execute(insert_queries.DAY_RECORD_INSERT_SUMMARY_SQL, (inserted_id,) + params)

            # レコードのインサート
            for record in data.records:
                params = record.insert_param_tuple()
                cursor.execute(insert_queries.RECORDS_INSERT_SQL, (inserted_id,) + params)

            self.conn.commit()

            logger.debug("data inserted: %s", inserted_id)
            return inserted_id
        except Exception as e:
            logger.error(e,exc_info=True)
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def select_piyolog(self, date: date) -> PiyoLogDayRecord:
        try:
            cursor = self.conn.cursor(dictionary=True)

            cursor.execute(select_queries.DAY_RECORD_SELECT_BY_DATE_SQL, (date,))

            row = cursor.fetchone()

            if row is None:
                logger.debug("Data not found for date: %s", date)
                return None

            logger.debug("Data fetched: %s", row)
            return PiyoLogDayRecord.from_dict(row)
        except Exception as e:
            logger.error(e,exc_info=True)
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def select_piyolog_id(self, date:date) -> int:
        try:
            cursor = self.conn.cursor(dictionary=True)

            cursor.execute(select_queries.DAY_RECORD_SELECT_BY_DATE_SQL, (date,))

            row = cursor.fetchone()

            if row is None:
                logger.debug("Data not found for date: %s", date)
                return None

            logger.debug("Data fetched: %s", row)
            return row["id"]
        except Exception as e:
            logger.error(e,exc_info=True)
            self.conn.rollback()
            raise e
        finally:
            cursor.close()