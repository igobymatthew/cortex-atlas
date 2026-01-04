from __future__ import annotations

from storage.database import init_db


def ensure_database() -> None:
    init_db()
