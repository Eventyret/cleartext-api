"""Endpoint for summarizing input text."""

from fastapi import APIRouter, HTTPException
from app.services.llm_provider import summarize
from pydantic import BaseModel, field_validator

router = APIRouter()


class SummarizeRequest(BaseModel):
    """Request payload with text to summarize and desired length."""

    text: str
    length: str = "short"

    @field_validator("length")
    @classmethod
    def validate_length(cls, v: str) -> str:
        """Ensure summary length is either 'short' or 'long'."""
        if v not in {"short", "long"}:
            raise ValueError("length must be 'short' or 'long'")
        return v


@router.post("")
async def summarize_text(req: SummarizeRequest):
    """Summarize text using the selected or fallback LLM provider.

    Args:
        payload (SummarizeRequest): Input text and summary length.

    Returns:
        dict: A JSON response with summary, provider, and fallback info.
    """
    try:
        return await summarize(req.text, req.length)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except TimeoutError:
        raise HTTPException(status_code=504, detail="LLM provider timeout")
    except Exception:
        raise HTTPException(status_code=500, detail="Summarization failed")
