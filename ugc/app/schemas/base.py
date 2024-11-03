import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class QualityChangeEvent(OrjsonBaseModel):
    event_type: str = "quality_change"
    user_id: int
    video_id: int
    old_quality: str
    new_quality: str
    timestamp: str


class VideoCompletedEvent(OrjsonBaseModel):
    event_type: str = "video_completed"
    user_id: int
    video_id: int
    timestamp: str


class SearchFilterEvent(OrjsonBaseModel):
    event_type: str = "search_filter"
    user_id: int
    filters: dict  # Словарь с фильтрами, например {"genre": "action", "rating": "9"}
    timestamp: str
