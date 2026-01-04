from fastapi import APIRouter

from backend.api.v1.analysis import router as analysis_router

router = APIRouter()
router.include_router(analysis_router, tags=["analysis"])
