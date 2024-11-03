from datetime import datetime
from uuid import UUID

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
    user_id: UUID4 = Field(default=None)
    video_id: UUID4
    old_quality: str
    new_quality: str
    timestamp: datetime


class VideoCompletedEvent(OrjsonBaseModel):
    event_type: str = "video_completed"
    user_id: UUID4 = Field(default=None)
    video_id: UUID4
    timestamp: datetime


class SearchFilterEvent(OrjsonBaseModel):
    event_type: str = "search_filter"
    user_id: UUID4 = Field(default=None)
    filters: dict  # Словарь с фильтрами, например {"genre": "action", "rating": "9"}
    timestamp: datetime


class PageTimeSpend(OrjsonBaseModel):
    event_type: str = "page_time_spend"
    user_id: UUID4 = Field(default=None)
    page_name: str
    entry_time: datetime
    exit_time: datetime = Field(default=None)


class UserPageClick(OrjsonBaseModel):
    event_type: str = "user_page_click"
    user_id: UUID4 = Field(default=None)
    session_id: str = Field(default=None)
    timestamp: datetime
    page_name: str
    element_id: int
    element_type: str
    referrer: str = None
    device: str = None
    browser: str = None
    location: str = None
