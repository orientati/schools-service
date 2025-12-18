from __future__ import annotations

import sys
import asyncio
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse

from app.api.v1.routes import school, citta, indirizzo, materia
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.db.base import import_models
from app.services import broker

import_models()  # Importo i modelli perché siano disponibili per le relazioni SQLAlchemy

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=True,
    release=settings.SENTRY_RELEASE,
)

logger = None


# RabbitMQ Broker
async def callback(message):
    async with message.process():
        print(
            f"Received message from exchange '{message.exchange}' with routing key '{message.routing_key}': {message.body.decode()}")


exchanges = {
    "schools": callback
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger = get_logger(__name__)
    logger.info(f"Starting {settings.SERVICE_NAME}...")

    # Avvia il broker asincrono all'avvio dell'app
    broker_instance = broker.AsyncBrokerSingleton()
    connected = False
    for i in range(settings.RABBITMQ_CONNECTION_RETRIES):
        logger.info(f"Connecting to RabbitMQ (attempt {i + 1}/{settings.RABBITMQ_CONNECTION_RETRIES})...")
        connected = await broker_instance.connect()
        if connected:
            break
        logger.warning(
            f"Failed to connect to RabbitMQ. Retrying in {settings.RABBITMQ_CONNECTION_RETRY_DELAY} seconds...")
        await asyncio.sleep(settings.RABBITMQ_CONNECTION_RETRY_DELAY)

    if not connected:
        logger.error("Could not connect to RabbitMQ after multiple attempts. Exiting...")
        sys.exit(1)

    else:
        logger.info("Connected to RabbitMQ.")
        for exchange, cb in exchanges.items():
            await broker_instance.subscribe(exchange, cb)

    yield

    logger.info(f"Shutting down {settings.SERVICE_NAME}...")
    await broker_instance.close()
    logger.info("RabbitMQ connection closed.")


docs_url = None if settings.ENVIRONMENT == "production" else "/docs"
redoc_url = None if settings.ENVIRONMENT == "production" else "/redoc"

app = FastAPI(
    title=settings.SERVICE_NAME,
    default_response_class=ORJSONResponse,
    version=settings.SERVICE_VERSION,
    lifespan=lifespan,
    docs_url=docs_url,
    redoc_url=redoc_url,
)

# Routers
current_router = APIRouter()

current_router.include_router(
    prefix="/schools",
    tags=[settings.SERVICE_NAME, "schools"],
    router=school.router,
)

current_router.include_router(
    prefix="/citta",
    tags=[settings.SERVICE_NAME, "citta"],
    router=citta.router,
)

current_router.include_router(
    prefix="/indirizzi",
    tags=[settings.SERVICE_NAME, "indirizzi"],
    router=indirizzo.router,
)

current_router.include_router(
    prefix="/materie",
    tags=[settings.SERVICE_NAME, "materie"],
    router=materia.router,
)
app.include_router(current_router, prefix=settings.API_PREFIX)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": settings.SERVICE_NAME}
