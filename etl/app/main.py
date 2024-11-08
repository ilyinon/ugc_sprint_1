import json
import time
from datetime import datetime
from multiprocessing import Process

import backoff
import clickhouse_connect
from config import KafkaTopics, etl_settings
from kafka import KafkaConsumer
from logger import logger
from pydantic import BaseModel, ValidationError

from schemas.base import (
    PageTimeSpend,
    QualityChangeEvent,
    SearchFilterEvent,
    UserPageClick,
    VideoCompletedEvent,
)

logger.info(f"kafka_bootstrap: {etl_settings.kafka_bootsrap}")

KAFKA_BROKERS = etl_settings.kafka_bootsrap

CLICKHOUSE_HOST = etl_settings.ch_host
CLICKHOUSE_PORT = etl_settings.ch_port
CLICKHOUSE_DATABASE = etl_settings.ch_database
CLICKHOUSE_USER = etl_settings.ch_user
CLICKHOUSE_PASSWORD = etl_settings.ch_password

poll_timeout = 10000  # in milliseconds
batch_size = 1000  # at least 1000 , https://clickhouse.com/docs/ru/introduction/performance#proizvoditelnost-pri-vstavke-dannykh
TIME_SLEEP = 0.1


clickhouse_client = clickhouse_connect.get_client(
    host=CLICKHOUSE_HOST,
    port=CLICKHOUSE_PORT,
    database=CLICKHOUSE_DATABASE,
    user=CLICKHOUSE_USER,
    password=CLICKHOUSE_PASSWORD,
)


def insert_data_to_clickhouse(name_table, data: list):
    logger.info(f"Inserting data: {data}")

    if data:
        try:
            clickhouse_client.insert(name_table, data)
            logger.info(f"Inserted {len(data)} rows to ClickHouse")
        except Exception as e:
            logger.error(f"Failed to insert data into ClickHouse: {e}")
    else:
        logger.info("No data to insert.")


@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=3,
)
def consume_messages(topic: str, model: BaseModel):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKERS,
        auto_offset_reset="earliest",
        group_id=f"group_{topic}",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        enable_auto_commit=False,
    )
    logger.info(f"Started consumer for topic: {topic}")

    while True:
        messages = consumer.poll(timeout_ms=poll_timeout, max_records=batch_size)

        for tp, msgs in messages.items():
            batch = []
            for message in msgs:
                try:
                    validated_data = model(**message.value)

                    if "entry_time" in message:
                        validated_data["entry_time"] = datetime.fromisoformat(
                            validated_data["entry_time"]
                        )
                    if "exit_time" in message:
                        validated_data["exit_time"] = datetime.fromisoformat(
                            validated_data["exit_time"]
                        )
                    row_data = [
                        getattr(validated_data, field)
                        for field in validated_data.model_fields
                    ]
                    batch.append(row_data)
                except ValidationError as e:
                    logger.error(f"Validation error in topic {topic}: {e}")
            if batch:
                insert_data_to_clickhouse(topic, batch)
                time.sleep(TIME_SLEEP)
                consumer.commit()


if __name__ == "__main__":
    topics = {
        KafkaTopics.PAGE_TIME_SPEND.value: PageTimeSpend,
        KafkaTopics.QUALITY_CHANGE.value: QualityChangeEvent,
        KafkaTopics.SEARCH_FILTER.value: SearchFilterEvent,
        KafkaTopics.USER_PAGE_CLICK.value: UserPageClick,
        KafkaTopics.VIDEO_COMPLETED.value: VideoCompletedEvent,
    }

    processes = []
    for topic, model in topics.items():
        process = Process(target=consume_messages, args=(topic, model))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
