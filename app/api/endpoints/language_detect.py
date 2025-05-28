"""Endpoint for detecting the language of input text."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from app.services.language import detect_language
from langdetect.lang_detect_exception import LangDetectException

router = APIRouter()


class LanguageDetectRequest(BaseModel):
    """Request body containing the text to detect language from."""

    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Ensure the input text is not empty or whitespace-only."""
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v


@router.post("/")
async def language_detect(req: LanguageDetectRequest):
    """Detect language of the provided input using langdetect.

    Args:
        payload (LanguageDetectRequest): Text for detection.

    Returns:
        dict: Language code and confidence score.
    """
    try:
        language = detect_language(req.text)

        if language == "unknown":
            raise HTTPException(
                status_code=422,
                detail="Could not determine language. Try providing more text.",
            )

        return {"language": language}

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    except HTTPException as e:
        raise e

    except LangDetectException:
        raise HTTPException(
            status_code=422,
            detail="Unable to detect language. Input might be too short or ambiguous.",
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Language detection failed")
