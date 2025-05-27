from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_provider import summarize

api_router = APIRouter()


class SummarizeRequest(BaseModel):
    text: str
    length: str = "short"


@api_router.post("/summarize")
async def summarize_text(req: SummarizeRequest):
    return await summarize(req.text, req.length)
