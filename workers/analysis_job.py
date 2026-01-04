from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, List

from backend.core.pipeline import run_pipeline
from storage.database import claim_next_job, init_db, update_job_status
from storage.vectors import store_report_vectors

logger = logging.getLogger(__name__)


def _parse_documents(raw_documents: Any) -> List[Dict[str, Any]]:
    if isinstance(raw_documents, str):
        return json.loads(raw_documents)
    if isinstance(raw_documents, list):
        return raw_documents
    return []


def run_worker_loop(poll_interval: float = 5.0) -> None:
    init_db()
    logger.info("Analysis worker started.")
    while True:
        job = claim_next_job()
        if not job:
            time.sleep(poll_interval)
            continue

        analysis_id = str(job["analysis_id"])
        subject_id = job.get("subject_id", "unknown")
        documents = _parse_documents(job.get("documents"))
        logger.info("Processing analysis job %s for subject %s", analysis_id, subject_id)

        try:
            report = run_pipeline(documents)
            report_payload = report.dict(by_alias=True)
            update_job_status(analysis_id, "completed", report=report_payload)
            store_report_vectors(subject_id, report_payload)
            logger.info("Completed analysis job %s", analysis_id)
        except Exception as exc:
            logger.exception("Failed analysis job %s", analysis_id)
            update_job_status(analysis_id, "failed", error=str(exc))
