import logging
import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import all_routers
from src.settings.database import migrate
from src.settings.logging_config import handler

logger: logging.Logger = logging.getLogger("root")
logger.addHandler(handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    migrate()
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
