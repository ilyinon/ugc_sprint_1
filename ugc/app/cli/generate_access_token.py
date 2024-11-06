from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt as jwt_auth

from core.config import ugc_settings
from core.logger import logger

user_data = {
    "user_id": str(uuid4()),
    "email": "user@ma.il",
    "roles": "user",
}


def create_token(user_data):

    expires_time = datetime.now(tz=timezone.utc) + timedelta(seconds=86400 * 30)
    payload = {
        "user_id": user_data["user_id"],
        "email": user_data["email"],
        "roles": user_data["roles"],
        "exp": expires_time,
        "jti": str(uuid4()),
    }
    token = jwt_auth.encode(
        payload=payload,
        key=ugc_settings.authjwt_secret_key,
        algorithm=ugc_settings.authjwt_algorithm,
    )
    logger.info("Token is generated")
    return token


if __name__ == "__main__":

    print(create_token(user_data))
