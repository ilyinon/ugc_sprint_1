from datetime import datetime, timedelta, timezone

from uuid import UUID, uuid4

import jwt as jwt_auth
from core.config import ugc_settings
from core.logger import logger

user_data = {
    "user_id": "3fa85f64-0000-1111-2222-2c963f66afa6",
    "email": "user@ma.il",
    "roles": "user"
}

def create_token(user_data):

    expires_time = datetime.now(tz=timezone.utc) + timedelta(
        seconds=86400
    )
    payload = {}

    payload["user_id"] = user_data["user_id"]
    payload["email"] = user_data["email"]
    payload["roles"] = user_data["roles"]
    payload["exp"] = expires_time
    payload["jti"] = str(uuid4())

    token = jwt_auth.encode(
        payload=payload,
        key=ugc_settings.authjwt_secret_key,
        algorithm=ugc_settings.authjwt_algorithm,
    )
    logger.info("Token is generated")
    return token


if __name__ == '__main__':
    print(create_token(user_data))