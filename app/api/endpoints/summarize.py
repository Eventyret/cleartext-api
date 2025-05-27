from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_provider import summarize

router = APIRouter()


class SummarizeRequest(BaseModel):
    text: str
    length: str = "short"


@router.post("/")
async def summarize_text(req: SummarizeRequest):
    try:
        return await summarize(req.text, req.length)
    except Exception:
        raise HTTPException(status_code=500, detail="Summarization failed")
