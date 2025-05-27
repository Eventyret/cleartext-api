from fastapi import APIRouter, HTTPException
from app.services.llm_provider import summarize
from pydantic import BaseModel, field_validator

router = APIRouter()


class SummarizeRequest(BaseModel):
    text: str
    length: str = "short"

    @field_validator("length")
    @classmethod
    def validate_length(cls, v: str) -> str:
        if v not in {"short", "long"}:
            raise ValueError("length must be 'short' or 'long'")
        return v


@router.post("/")
async def summarize_text(req: SummarizeRequest):
    try:
        return await summarize(req.text, req.length)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except TimeoutError:
        raise HTTPException(status_code=504, detail="LLM provider timeout")
    except Exception:
        raise HTTPException(status_code=500, detail="Summarization failed")
