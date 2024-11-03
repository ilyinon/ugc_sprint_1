import orjson
from pydantic import BaseModel, Field, UUID4
from uuid import UUID
from datetime import datetime



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
