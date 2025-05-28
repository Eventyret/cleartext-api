"""OpenAI wrapper for summarization, rewriting, and title generation."""

import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY
MODEL_IDS = {
    "4o-mini": "gpt-4o-mini",
    "4.1-mini": "gpt-4.1-mini",
    "o3-mini": "o3-mini",
}


def get_model(variant: str = "3.5") -> str:
    """Return the OpenAI model name based on the specified variant."""
    return MODEL_IDS.get(variant, MODEL_IDS["3.5"])


async def summarize(text: str, length: str = "short", variant: str = "3.5") -> str:
    """Summarize input text using the selected OpenAI model."""
    prompt = f"Summarize the following text in a {length} way:\n\n{text}"
    response = await openai.ChatCompletion.acreate(
        model=get_model(variant),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


async def rewrite(text: str, style: str = "simple", variant: str = "3.5") -> str:
    """Rewrite input text using the specified tone and OpenAI model."""
    prompt = f"Rewrite this text in a more {style} tone:\n\n{text}"
    response = await openai.ChatCompletion.acreate(
        model=get_model(variant),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


async def generate_title(text: str, variant: str = "3.5") -> str:
    """Generate a concise title using the selected OpenAI model."""
    prompt = f"Create a short, engaging title for:\n\n{text}"
    response = await openai.ChatCompletion.acreate(
        model=get_model(variant),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip().strip('"')
