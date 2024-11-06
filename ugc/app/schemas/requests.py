from datetime import datetime

import orjson
from pydantic import UUID4, BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class QualityChangeEvent(OrjsonBaseModel):
    event_type: str = "quality_change"
    video_id: UUID4
    old_quality: str
    new_quality: str
    timestamp: datetime


class VideoCompletedEvent(OrjsonBaseModel):
    event_type: str = "video_completed"
    video_id: UUID4
    timestamp: datetime


class SearchFilterEvent(OrjsonBaseModel):
    event_type: str = "search_filter"
    filters: dict  # Словарь с фильтрами, например {"genre": "action", "rating": "9"}
    timestamp: datetime


class PageTimeSpend(OrjsonBaseModel):
    event_type: str = "page_time_spend"
    page_name: str
    entry_time: datetime
    exit_time: datetime = Field(default=None)


class UserPageClick(OrjsonBaseModel):
    event_type: str = "user_page_click"
    session_id: str = Field(default=None)
    timestamp: datetime
    page_name: str
    element_id: int
    element_type: str
