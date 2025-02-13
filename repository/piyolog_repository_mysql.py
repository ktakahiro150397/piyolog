
from datetime import date
from logger_factory import LoggerFactory
from model.piyolog_day_record import PiyoLogDayRecord
from repository.piyolog_repository_base import PiyologRepositoryBase

logger = LoggerFactory.getLogger(__name__)

MYSQL_DELETE_SQL = """
DELETE FROM day_record
WHERE
    date = %s;
"""

MYSQL_INSERT_SQL = """
INSERT INTO day_record (
    date,
    daily_memo
) VALUES (
    %s,
    %s
);
"""

MYSQL_SELECT_SQL = """
SELECT *
FROM day_record
WHERE
    date = %s;
"""

class PiyologRepositoryMySql(PiyologRepositoryBase):
    def __init__(self,conn ):
        self.conn = conn

    def delete_insert_piyolog(self, data: PiyoLogDayRecord) -> int:
        try:
            cursor = self.conn.cursor()

            params = data.insert_param_tuple()
            cursor.execute(MYSQL_DELETE_SQL, (params[0],))

            cursor.execute(MYSQL_INSERT_SQL, params)

            inserted_id = cursor.lastrowid
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

            cursor.execute(MYSQL_SELECT_SQL, (date,))

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
