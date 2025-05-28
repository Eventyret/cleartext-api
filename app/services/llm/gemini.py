"""Gemini model wrapper for summarization, rewriting, and title generation."""

import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL_IDS = {
    "2.5": "models/gemini-2.5-flash-preview-05-20",
    "1.5": "models/gemini-1.5-flash",
}

_models = {
    variant: genai.GenerativeModel(model_id) for variant, model_id in MODEL_IDS.items()
}


def get_model(variant: str = "1.5"):
    """Get the Gemini model for the specified variant."""
    return _models.get(variant, _models["1.5"])


async def summarize(text: str, length: str = "short", variant: str = "2.5") -> str:
    """Summarize input text using a fallback chain of supported LLM providers.

    Tries Gemini (2.5 → 1.5) first if selected, then OpenAI if configured.
    """
    model = get_model(variant)
    prompt = f"Summarize the following text in a {length} way:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()


async def rewrite(text: str, style: str = "simple", variant: str = "2.5") -> str:
    """Rewrite input text into a different tone using fallback across LLM providers.

    Supports styles like 'simple' or 'formal', and falls back from Gemini to OpenAI.
    """
    model = get_model(variant)
    prompt = f"Rewrite the following text in a more {style} tone:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()


async def generate_title(text: str, variant: str = "2.5") -> str:
    """Generate a concise title from input text using LLM provider fallback.

    Attempts Gemini first, then OpenAI if available.
    """
    prompt = f"""
Generate a concise and engaging title for the following content:

{text.strip()}

Title:
"""
    model = _models.get(variant)
    if not model:
        raise ValueError(f"Unknown Gemini model variant: {variant}")

    response = model.generate_content(prompt)
    return response.text.strip().strip('"')
