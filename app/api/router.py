from fastapi import APIRouter
from app.api.endpoints import language_detect, summarize, title
from app.api.endpoints import rewrite

api_router = APIRouter()

api_router.include_router(summarize.router, prefix="/summarize", tags=["Summarize"])

api_router.include_router(rewrite.router, prefix="/rewrite", tags=["Rewrite"])
api_router.include_router(title.router, prefix="/title", tags=["Title"])
api_router.include_router(
    language_detect.router, prefix="/language-detect", tags=["Language"]
)
