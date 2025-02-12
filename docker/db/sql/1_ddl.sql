-- CREATE DATABASE IF NOT EXISTS piyolog;
USE piyolog;

CREATE TABLE IF NOT EXISTS day_record (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    daily_memo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS day_record_summary (
    id INT PRIMARY KEY AUTO_INCREMENT,
    day_record_id INT,
    bleast_feed_time_left INT,
    bleast_feed_time_right INT,
    formula_count INT,
    formula_total_amount INT,
    sleep_duration_seconds INT,
    pee_count INT,
    poo_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_day_record_summary FOREIGN KEY (day_record_id) REFERENCES day_record(id)
);

CREATE TABLE IF NOT EXISTS records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    day_record_id INT,
    record_type TEXT NOT NULL,
    additional_record_data TEXT,
    record_memo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_record_day_record FOREIGN KEY (day_record_id) REFERENCES day_record(id)
);
