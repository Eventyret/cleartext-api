from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from app.services.llm_provider import rewrite

router = APIRouter()


class RewriteRequest(BaseModel):
    text: str
    style: str = "simple"

    @field_validator("style")
    @classmethod
    def validate_style(cls, v: str) -> str:
        if v not in {"simple", "formal"}:
            raise ValueError("style must be 'simple' or 'formal'")
        return v


@router.post("/")
async def rewrite_text(req: RewriteRequest):
    try:
        return await rewrite(req.text, req.style)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except TimeoutError:
        raise HTTPException(status_code=504, detail="LLM provider timeout")
    except Exception:
        raise HTTPException(status_code=500, detail="Rewrite failed")
