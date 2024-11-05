import os
from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict

from ugc.app.core.logger import LOGGING

DOTENV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".env"))

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UgcSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV, extra='ignore')

    project_name: str = "ugc"

    authjwt_secret_key: str
    authjwt_algorithm: str = "HS256"

    kafka_bootsrap: str = "localhost:9094,localhost:9095,localhost:9096"
    kafka_topics: list = [
        "track_events",
        "quality_change",
        "video_completed",
        "search_filter",
        "page_time_spend",
        "user_page_click",
    ]

    log_level: bool = False


ugc_settings = UgcSettings()


def get_config():
    return UgcSettings()
