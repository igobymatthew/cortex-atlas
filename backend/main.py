from __future__ import annotations

from fastapi import FastAPI

from backend.api.v1 import analysis, health, results
from backend.config import load_settings

settings = load_settings()

app = FastAPI(title="Cortex Atlas", version="0.1.0")
app.include_router(analysis.router, prefix=settings.api_prefix, tags=["analysis"])
app.include_router(results.router, prefix=settings.api_prefix, tags=["reports"])
app.include_router(health.router, prefix=settings.api_prefix, tags=["health"])
