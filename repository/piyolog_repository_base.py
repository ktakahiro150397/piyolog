from datetime import date
from model.piyolog_day_record import PiyoLogDayRecord


class PiyologRepositoryBase():
    def __init__(self):
        pass

    def delete_insert_piyolog(self, data: PiyoLogDayRecord) -> int:
        raise NotImplementedError("This method must be called from a concrete class.")
    
    def select_piyolog(self, date: date) -> PiyoLogDayRecord:
        raise NotImplementedError("This method must be called from a concrete class.")