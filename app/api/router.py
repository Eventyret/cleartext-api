from fastapi import APIRouter
from app.api.endpoints import summarize

api_router = APIRouter()
api_router.include_router(summarize.router, prefix="/summarize", tags=["Summarize"])
