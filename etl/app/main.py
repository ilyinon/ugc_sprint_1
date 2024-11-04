import datetime
import json

import clickhouse_connect
from config import etl_settings
from logger import logger

from kafka import KafkaConsumer

logger.info(f"kafka_bootstrap: {etl_settings.kafka_bootsrap}")
KAFKA_BROKERS = etl_settings.kafka_bootsrap
KAFKA_TOPIC = "quality_change"

# Настройка подключения к ClickHouse
CLICKHOUSE_HOST = etl_settings.ch_host
CLICKHOUSE_PORT = etl_settings.ch_port
CLICKHOUSE_DATABASE = etl_settings.ch_database
CLICKHOUSE_USER = etl_settings.ch_user
CLICKHOUSE_PASSWORD = etl_settings.ch_password


clickhouse_client = clickhouse_connect.get_client(
    host=CLICKHOUSE_HOST,
    port=CLICKHOUSE_PORT,
    database=CLICKHOUSE_DATABASE,
    user=CLICKHOUSE_USER,
    password=CLICKHOUSE_PASSWORD,
)


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKERS,
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="lets-upload-it2",
)


for message in consumer:
    logger.info(f"message.value: {message.value}")
    data = message.value

    timestamp_obj = datetime.datetime.fromisoformat(data["timestamp"])

    clickhouse_data = [
        data["event_type"],
        data["user_id"],
        data["video_id"],
        data["old_quality"],
        data["new_quality"],
        timestamp_obj,
    ]
    to_insert = [
        clickhouse_data,
    ]
    column_names = [
        "event_type",
        "user_id",
        "video_id",
        "old_quality",
        "new_quality",
        "timestamp",
    ]

    logger.info(f"clickhouse_data {clickhouse_data}")
    clickhouse_client.insert("quality_change", to_insert)
