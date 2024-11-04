CREATE DATABASE IF NOT EXISTS actions_users;

USE actions_users;

CREATE TABLE IF NOT EXISTS my_table (
    event_type String,
    user_id UUID NOT NULL,
    video_id UUID NOT NULL,
    old_quality String,
    new_quality String,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY timestamp;


