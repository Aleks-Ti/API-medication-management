import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.event.dependencies import event_service as _event_service
from src.event.setup import setup_queue
from src.routers import all_routers
from src.settings.database import migrate
from src.settings.logging_config import handler

logger: logging.Logger = logging.getLogger("root")
logger.addHandler(handler)

event_service = _event_service()


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(event_service.scan_event())
    await migrate()
    setup_queue()
    yield


if os.environ.get("ENV") == "prod":
    logger.setLevel(logging.ERROR)
    app = FastAPI(
        title="Podvig Api",
        openapi_url=None,
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )
else:
    logger.setLevel(logging.INFO)
    app = FastAPI(
        title="Podvig Api",
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        lifespan=lifespan,
    )


api = APIRouter(
    prefix="/api",
    responses={404: {"description": "Page not found"}},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


for router in all_routers:
    api.include_router(router)

app.include_router(api)
