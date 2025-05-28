"""Endpoint for generating a title from provided content."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from app.services.llm_provider import generate_title

router = APIRouter()


class TitleRequest(BaseModel):
    """Request payload containing the text to generate a title for."""

    text: str = Field(..., json_schema_extra={"example": "Here is a long article..."})

    @field_validator("text")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        """Validate that the input text is not empty or whitespace only."""
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v


class TitleResponse(BaseModel):
    """Response payload containing the generated title."""

    title: str


@router.post("/", response_model=TitleResponse)
async def title_route(payload: TitleRequest):
    """Generate a title for the given text using provider fallback chain.

    Args :
        payload (TitleRequest): Input text to generate a title for.

    Returns:
        dict: A response with generated title and metadata.
    """
    try:
        title = await generate_title(payload.text)
        return TitleResponse(title=title)
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(
            status_code=500, detail="Internal server error during title generation"
        )
