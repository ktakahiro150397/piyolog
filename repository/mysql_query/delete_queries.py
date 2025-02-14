
DAY_RECORD_DELETE_SQL = """
DELETE FROM day_record
WHERE
    id = %s;
"""

DAY_RECORD_SUMMARY_DELETE_SQL = """
DELETE FROM day_record_summary
WHERE
    day_record_id = %s;
"""

RECOREDS_DELETE_SQL = """
DELETE FROM records
WHERE
    day_record_id = %s;
"""
