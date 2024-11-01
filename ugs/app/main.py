import uuid

from api.v1 import click
from core.config import ugs_settings
from core.tracer import configure_tracer
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(
    title=ugs_settings.project_name,
    docs_url="/api/v1/ugs/openapi",
    openapi_url="/api/v1/ugs/openapi.json",
    default_response_class=ORJSONResponse,
)

if ugs_settings.enable_tracer:
    configure_tracer()
    FastAPIInstrumentor.instrument_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    pass


@app.middleware("http")
async def before_request(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        request_id = str(uuid.uuid4())
    # if not request_id:
    #     return ORJSONResponse(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         content={"detail": "X-Request-Id is required"},
    #     )
    return await call_next(request)


# @app.get("/api/openapi", include_in_schema=False)
# async def get_documentation():
#     return get_swagger_ui_html(openapi_url="/api/openapi.json", title="Swagger")

app.include_router(click.router, prefix="/api/v1/click")
