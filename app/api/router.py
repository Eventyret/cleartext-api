from fastapi import APIRouter
from app.api.endpoints import summarize
from app.api.endpoints import rewrite

api_router = APIRouter()
api_router.include_router(summarize.router, prefix="/summarize", tags=["Summarize"])

api_router.include_router(rewrite.router, prefix="/rewrite", tags=["Rewrite"])
