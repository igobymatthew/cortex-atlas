from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

from backend.core.pipeline import run_pipeline
from storage.database import claim_next_job, update_job_status

logger = logging.getLogger(__name__)


def _coerce_documents(value: Any) -> Any:
    if isinstance(value, str):
        return json.loads(value)
    return value


def run_once() -> Optional[str]:
    job = claim_next_job()
    if not job:
        return None

    analysis_id = str(job["analysis_id"])
    try:
        documents = _coerce_documents(job.get("documents", []))
        report = run_pipeline(documents)
        if hasattr(report, "model_dump"):
            payload: Dict[str, Any] = report.model_dump(by_alias=True)
        else:
            payload = report.dict(by_alias=True)
        update_job_status(analysis_id, "completed", report=payload)
        logger.info("Completed analysis job %s", analysis_id)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Analysis job %s failed", analysis_id)
        update_job_status(analysis_id, "failed", error=str(exc))
    return analysis_id


def main() -> None:
    processed = run_once()
    if processed is None:
        logger.info("No queued analysis jobs available.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
