import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".env"))

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UgcSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    project_name: str = "ugc"


    authjwt_secret_key: str
    authjwt_algorithm: str = "HS256"


    kafka_bootsrap: str = "kafka-0:9092,kafka-1:9092,kafka-2:9092"
    kafka_topics: list = ["track_events", 
                          "quality_change", 
                          "video_completed", 
                          "search_filter",
                          "page_time_spend",
                          "user_page_click"]


    log_level: bool = False



ugc_settings = UgcSettings()


def get_config():
    return UgcSettings()
