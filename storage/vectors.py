from __future__ import annotations

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def store_report_vectors(subject_id: str, report: Dict[str, Any]) -> None:
    logger.info(
        "Vector storage not configured. Skipping vector persistence for subject %s.",
        subject_id,
    )
