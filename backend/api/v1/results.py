from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from storage.database import fetch_job

router = APIRouter()


def _normalize_report(job: Dict[str, Any]) -> Dict[str, Any]:
    report = job.get("report")
    if report is None:
        raise HTTPException(status_code=404, detail="Report not available yet")
    return report


@router.get("/analysis/{analysis_id}")
def get_analysis_status(analysis_id: str) -> Dict[str, Any]:
    job = fetch_job(analysis_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found")
    return {
        "analysis_id": job["analysis_id"],
        "status": job["status"],
    }


@router.get("/reports/{analysis_id}")
def get_report(analysis_id: str) -> Dict[str, Any]:
    job = fetch_job(analysis_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found")
    return _normalize_report(job)
