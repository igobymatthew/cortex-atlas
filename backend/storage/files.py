from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path("storage_artifacts")


def persist_report(report_id: str, payload: Dict[str, Any]) -> Path:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    path = BASE_DIR / f"{report_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def load_report(report_id: str) -> Dict[str, Any]:
    path = BASE_DIR / f"{report_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))
