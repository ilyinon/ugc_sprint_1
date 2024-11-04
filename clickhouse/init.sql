CREATE DATABASE IF NOT EXISTS user_actions;

USE user_actions;

CREATE TABLE IF NOT EXISTS quality_change (
    event_type String,
    user_id UUID NOT NULL,
    video_id UUID NOT NULL,
    old_quality String,
    new_quality String,
    timestamp DateTime NOT NULL
) ENGINE = MergeTree()
ORDER BY timestamp;


CREATE TABLE IF NOT EXISTS video_completed(
    event_type String,
    user_id UUID NOT NULL,
    video_id UUID NOT NULL,
    timestamp DateTime NOT NULL
) ENGINE = MergeTree()
ORDER BY timestamp;

CREATE TABLE IF NOT EXISTS search_filter(
    event_type String,
    user_id UUID NOT NULL,
    filters Map(String, String),
    timestamp DateTime NOT NULL
)
ORDER BY timestamp;

CREATE TABLE IF NOT EXISTS page_time_spend(
    event_type String,
    user_id UUID NOT NULL,
    page_name String,
    entry_time DateTime NOT NULL,
    exit_time DateTime
) ENGINE = MergeTree()
ORDER BY entry_time;


CREATE TABLE IF NOT EXISTS user_interaction(
    event_type String,
    user_id UUID NOT NULL,
    session_id String,
    timestamp DateTime NOT NULL,
    page_name String,
    element_id Int64,
    elemeny_type String
) ENGINE = MergeTree()
ORDER BY timestamp;
