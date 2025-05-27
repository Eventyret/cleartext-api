from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from app.services.llm_provider import rewrite

router = APIRouter()


class RewriteRequest(BaseModel):
    """Request payload with the text to rewrite and desired style."""

    text: str
    style: str = "simple"

    @field_validator("style")
    @classmethod
    def validate_style(cls, v: str) -> str:
        """Ensure style is either 'simple' or 'formal'."""
        if v not in {"simple", "formal"}:
            raise ValueError("style must be 'simple' or 'formal'")
        return v


@router.post("/")
async def rewrite_text(req: RewriteRequest):
    """
    Rewrite the input text using the specified style.

    Style can be 'simple' or 'formal'.
    """
    try:
        return await rewrite(req.text, req.style)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except TimeoutError:
        raise HTTPException(status_code=504, detail="LLM provider timeout")
    except Exception:
        raise HTTPException(status_code=500, detail="Rewrite failed")
