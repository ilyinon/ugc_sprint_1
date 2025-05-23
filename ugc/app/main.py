from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import track_event
from core.config import ugc_settings

app = FastAPI(
    title=ugc_settings.project_name,
    docs_url="/api/v1/ugc/openapi",
    openapi_url="/api/v1/ugc/openapi.json",
    default_response_class=ORJSONResponse,
)


app.include_router(track_event.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Track events"}
