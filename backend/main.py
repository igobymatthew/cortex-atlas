from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.api.v1 import analysis, health, results
from backend.config import load_settings

settings = load_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup hooks (DB, vector store, queues) go here
    yield
    # Shutdown hooks go here


app = FastAPI(
    title="Cortex Atlas",
    version="0.1.0",
    lifespan=lifespan,
)

API_V1_PREFIX = f"{settings.api_prefix}/v1"

app.include_router(
    analysis.router,
    prefix=API_V1_PREFIX,
    tags=["analysis"],
)

app.include_router(
    results.router,
    prefix=API_V1_PREFIX,
    tags=["reports"],
)

app.include_router(
    health.router,
    prefix=API_V1_PREFIX,
    tags=["health"],
)


@app.get("/")
def root():
    return {
        "service": "cortex-atlas",
        "version": app.version,
        "status": "running",
    }
