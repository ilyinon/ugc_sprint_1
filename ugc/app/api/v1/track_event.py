import json
import os

import jwt
from core.config import ugc_settings
from core.logger import logger
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.base import QualityChangeEvent, SearchFilterEvent, VideoCompletedEvent

from kafka import KafkaProducer

security = HTTPBearer()

# Настройки Kafka (можно вынести в .env файл)


# Создаем Kafka producer
producer = KafkaProducer(
    bootstrap_servers=ugc_settings.kafka_bootsrap,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


router = APIRouter()


async def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)):
    logger.info("Got token")
    try:
        payload = jwt.decode(
            credentials.credentials, 
            ugc_settings.authjwt_secret_key, 
            algorithms=[ugc_settings.authjwt_secret_key]
        )
        return payload
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT token expired")


@router.post("/track_event", response_model=None, summary="Track events")
async def track_event(
    event: QualityChangeEvent | VideoCompletedEvent | SearchFilterEvent,
    # payload: dict = Depends(verify_jwt),
):
    """
    Get events from users.
    """
    if event.event_type in ugc_settings.kafka_topics:
        kafka_topic = event.event_type
    else:
        logger.error(f"Wrong kafka topic {event.event_type}")
        raise HTTPException(status_code=500, detail=f"Error tracking event")
    try:
        # event_to_save = event["email"] = payload["email"]
        # Send events to Kafka
        event_to_save = event
        producer.send(kafka_topic, event_to_save.dict())
        producer.flush()

    except Exception as e:
        logger.error(f"Event didn't track successfully")
        raise HTTPException(status_code=500, detail=f"Error tracking event: {str(e)}")
