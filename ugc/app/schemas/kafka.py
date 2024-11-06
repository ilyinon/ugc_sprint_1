from datetime import datetime

import orjson
from pydantic import UUID4, BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class KafkaQualityChangeEvent(OrjsonBaseModel):
    event_type: str = "quality_change"
    user_id: UUID4
    video_id: UUID4
    old_quality: str
    new_quality: str
    timestamp: datetime


class KafkaVideoCompletedEvent(OrjsonBaseModel):
    event_type: str = "video_completed"
    user_id: UUID4
    video_id: UUID4
    timestamp: datetime


class KafkaSearchFilterEvent(OrjsonBaseModel):
    event_type: str = "search_filter"
    user_id: UUID4
    filters: dict  # Словарь с фильтрами, например {"genre": "action", "rating": "9"}
    timestamp: datetime


class KafkaPageTimeSpend(OrjsonBaseModel):
    event_type: str = "page_time_spend"
    user_id: UUID4
    page_name: str
    entry_time: datetime
    exit_time: datetime = Field(default=None)


class KafkaUserPageClick(OrjsonBaseModel):
    event_type: str = "user_page_click"
    user_id: UUID4
    session_id: str = Field(default=None)
    timestamp: datetime
    page_name: str
    element_id: int
    element_type: str
