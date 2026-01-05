from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_prefix: str
    environment: str
    log_level: str
    database_url: str


def load_settings() -> Settings:
    return Settings(
        api_prefix=os.environ.get("API_PREFIX", "/api/v1"),
        environment=os.environ.get("ENVIRONMENT", "development"),
        log_level=os.environ.get("LOG_LEVEL", "info"),
        database_url=os.environ.get(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cortex_atlas"
        ),
    )
