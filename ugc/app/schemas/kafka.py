import orjson
from pydantic import UUID4, BaseModel

from .requests import (
    PageTimeSpend,
    QualityChangeEvent,
    SearchFilterEvent,
    UserPageClick,
    VideoCompletedEvent,
)


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UserIdMixin(OrjsonBaseModel):
    user_id: UUID4


class KafkaQualityChangeEvent(QualityChangeEvent, UserIdMixin):
    pass


class KafkaVideoCompletedEvent(VideoCompletedEvent, UserIdMixin):
    pass


class KafkaSearchFilterEvent(SearchFilterEvent, UserIdMixin):
    pass


class KafkaPageTimeSpend(PageTimeSpend, UserIdMixin):
    pass


class KafkaUserPageClick(UserPageClick, UserIdMixin):
    pass
