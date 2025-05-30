"""API router that aggregates all endpoint routes."""

from fastapi import APIRouter, Depends
from app.api.endpoints import language_detect, summarize, title
from app.api.endpoints import rewrite
from app.core.security import verify_internal_api_key

api_router = APIRouter(dependencies=[Depends(verify_internal_api_key)])

api_router.include_router(summarize.router, prefix="/summarize", tags=["Summarize"])

api_router.include_router(rewrite.router, prefix="/rewrite", tags=["Rewrite"])
api_router.include_router(title.router, prefix="/title", tags=["Title"])
api_router.include_router(
    language_detect.router, prefix="/language-detect", tags=["Language"]
)
