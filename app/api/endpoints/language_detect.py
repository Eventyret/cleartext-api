from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from app.services.language import detect_language
from langdetect.lang_detect_exception import LangDetectException

router = APIRouter()


class LanguageDetectRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v


@router.post("/")
async def language_detect(req: LanguageDetectRequest):
    try:
        language = detect_language(req.text)

        if language == "unknown":
            raise HTTPException(
                status_code=422,
                detail="Could not determine language — try providing more text",
            )

        return {"language": language}

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    except HTTPException as e:
        raise e  # Don't double-wrap

    except LangDetectException:
        raise HTTPException(
            status_code=422,
            detail="Unable to detect language. Input might be too short or ambiguous.",
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Language detection failed")
