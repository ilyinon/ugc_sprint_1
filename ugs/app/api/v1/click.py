from random import randint
from typing import Annotated, List, Literal, LiteralString, Optional, Union
from uuid import UUID

from core.logger import logger
from fastapi import APIRouter, Body, Depends, Request, Response, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, OAuth2AuthorizationCodeBearer
from fastapi.responses import ORJSONResponse

get_token = HTTPBearer(auto_error=False)


router = APIRouter()


@router.post(
    "/click",
    response_model=None,
    summary="User login",
    tags=["UGS"],
)
async def login(
    request: Request,
    response: Response,

):
    """
    Get clicks from users.
    """
    logger.info(f"Requested /click")
    return ORJSONResponse(status_code=200)
