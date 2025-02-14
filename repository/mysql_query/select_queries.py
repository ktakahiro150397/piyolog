DAY_RECORD_SELECT_BY_DATE_SQL = """
SELECT *
FROM day_record
WHERE
    date = %s;
"""