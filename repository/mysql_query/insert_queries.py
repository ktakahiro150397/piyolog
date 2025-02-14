DAY_RECORD_INSERT_SQL = """
INSERT INTO day_record (
    date,
    daily_memo
) VALUES (
    %s,
    %s
);
"""

DAY_RECORD_INSERT_SUMMARY_SQL = """
INSERT INTO day_record_summary (
    day_record_id,
    bleast_feed_time_left,
    bleast_feed_time_right,
    formula_count,
    formula_total_amount,
    sleep_duration_seconds,
    pee_count,
    poo_count
) VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
);
"""