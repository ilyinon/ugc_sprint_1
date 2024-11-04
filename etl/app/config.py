import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".env"))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class EtlSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    kafka_bootsrap: list = ["kafka-0:9092", "kafka-1:9092", "kafka-2:9092"]
    kafka_topics: list = [
        "track_events",
        "quality_change",
        "video_completed",
        "search_filter",
        "page_time_spend",
        "user_page_click",
    ]

    ch_host: str = "clickhouse"
    ch_port: int = 8123
    ch_database: str = "user_actions"
    ch_user: str = "default"
    ch_password: str = ""

    log_level: bool = False


etl_settings = EtlSettings()


def get_config():
    return EtlSettings()
