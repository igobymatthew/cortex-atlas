from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from backend.api.deps import ensure_database
from backend.core.schemas import Input
from storage.database import enqueue_analysis_job

router = APIRouter()


class AnalysisOptions(BaseModel):
    language: Optional[str] = None
    retain_raw_text: bool = False
    confidence_threshold: Optional[float] = None


class AnalysisRequest(BaseModel):
    subject_id: str
    documents: List[Input]
    options: Optional[AnalysisOptions] = None


class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str = Field(default="queued")
    estimated_time_seconds: int = Field(default=45)


@router.post("/analysis", response_model=AnalysisResponse, status_code=202)
def create_analysis_job(
    payload: AnalysisRequest,
    _: None = Depends(ensure_database),
) -> AnalysisResponse:
    analysis_id = enqueue_analysis_job(
        payload.subject_id,
        [document.dict() for document in payload.documents],
        payload.options.dict() if payload.options else None,
    )
    return AnalysisResponse(analysis_id=analysis_id)
