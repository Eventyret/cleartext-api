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
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v


class TitleResponse(BaseModel):
    """Response payload containing the generated title."""

    title: str


@router.post("/", response_model=TitleResponse)
async def title_route(payload: TitleRequest):
    """
    Generate a concise title for the provided text using the language model.

    Returns a generated title string. Falls back if the primary model fails.
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
