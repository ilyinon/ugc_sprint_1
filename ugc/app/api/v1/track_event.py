import json

import jwt
from fastapi import APIRouter, Depends, Security
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from kafka import KafkaProducer

from core.config import ugc_settings
from core.logger import logger
from schemas.kafka import (
    KafkaPageTimeSpend,
    KafkaQualityChangeEvent,
    KafkaSearchFilterEvent,
    KafkaUserPageClick,
    KafkaVideoCompletedEvent,
)
from schemas.requests import (
    PageTimeSpend,
    QualityChangeEvent,
    SearchFilterEvent,
    UserPageClick,
    VideoCompletedEvent,
)

security = HTTPBearer()


producer = KafkaProducer(
    bootstrap_servers=ugc_settings.kafka_bootsrap,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


router = APIRouter()


async def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify user's token and get its payload.
    """
    try:
        payload = jwt.decode(
            credentials.credentials,
            ugc_settings.authjwt_secret_key,
            algorithms=[ugc_settings.authjwt_algorithm],
        )
        return payload
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT token expired")


event_types = {
    "quality_change": KafkaQualityChangeEvent,
    "video_completed": KafkaVideoCompletedEvent,
    "search_filter": KafkaSearchFilterEvent,
    "page_time_spend": KafkaPageTimeSpend,
    "user_page_click": KafkaUserPageClick,
}


@router.post("/track_event", response_model=None, summary="Track events")
async def track_event(
    event: (
        QualityChangeEvent
        | VideoCompletedEvent
        | SearchFilterEvent
        | PageTimeSpend
        | UserPageClick
    ),
    payload: dict = Depends(verify_jwt),
):
    """
    Get events from users.
    """
    logger.debug("event: %s", event)
    logger.debug("payload: %s", payload["user_id"])
    if event.event_type in ugc_settings.kafka_topics:
        kafka_topic = event.event_type
    else:
        logger.error(f"Wrong kafka topic {event.event_type}")
        raise HTTPException(status_code=500, detail="Error tracking event")
    try:

        event_to_save = event.dict()
        event_to_save["user_id"] = payload["user_id"]

        event_type = event_to_save["event_type"]
        event_to_kafa = event_types.get(event_type, None)(**event_to_save)

        producer.send(kafka_topic, event_to_kafa.model_dump(mode="json"))
        producer.flush()

    except Exception as e:
        logger.error(f"Event didn't track successfully, {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error tracking event: {str(e)}")
