import os
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".env"))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class KafkaTopics(Enum):
    TRACK_EVENTS = "track_events"
    QUALITY_CHANGE = "quality_change"
    VIDEO_COMPLETED = "video_completed"
    SEARCH_FILTER = "search_filter"
    PAGE_TIME_SPEND = "page_time_spend"
    USER_PAGE_CLICK = "user_page_click"


class EtlSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    kafka_bootsrap: list = ["kafka-0:9092", "kafka-1:9092", "kafka-2:9092"]
    ch_host: str = "clickhouse"
    ch_port: int = 8123
    ch_database: str = "actions_users"
    ch_user: str = "default"
    ch_password: str = ""

    log_level: bool = False


etl_settings = EtlSettings()
