"""LLM provider orchestrator with fallback across providers."""

from fastapi import HTTPException
from app.core.config import settings
from app.services.llm import gemini, openai


async def fallback_chain(operations):
    """Attempt multiple providers in order, returning the first successful result."""
    for provider, fn in operations:
        try:
            return await fn(), provider
        except Exception:
            continue
    raise HTTPException(status_code=503, detail="All providers failed")


async def summarize(text: str, length: str = "short") -> dict:
    """Summarize input text using selected provider fallback."""
    chain = []

    if settings.LLM_PROVIDER == "gemini":
        chain += [
            ("gemini-2.5", lambda: gemini.summarize(text, length, "2.5")),
            ("gemini-1.5", lambda: gemini.summarize(text, length, "1.5")),
        ]

    if settings.OPENAI_API_KEY:
        chain += [
            ("openai-4o-mini", lambda: openai.summarize(text, length, "4o-mini")),
            ("openai-4.1-mini", lambda: openai.summarize(text, length, "4.1-mini")),
            ("openai-o3-mini", lambda: openai.summarize(text, length, "o3-mini")),
        ]

    result, provider = await fallback_chain(chain)
    return {"summary": result, "provider": provider}


async def rewrite(text: str, style: str = "simple") -> dict:
    """Rewrite text with selected provider fallback."""
    chain = []

    if settings.LLM_PROVIDER == "gemini":
        chain += [
            ("gemini-2.5", lambda: gemini.rewrite(text, style, "2.5")),
            ("gemini-1.5", lambda: gemini.rewrite(text, style, "1.5")),
        ]

    if settings.OPENAI_API_KEY:
        chain += [
            ("openai-4o-mini", lambda: openai.rewrite(text, style, "4o-mini")),
            ("openai-4.1-mini", lambda: openai.rewrite(text, style, "4.1-mini")),
            ("openai-o3-mini", lambda: openai.rewrite(text, style, "o3-mini")),
        ]

    result, provider = await fallback_chain(chain)
    return {"rewritten": result, "provider": provider}


async def generate_title(text: str) -> str:
    """Generate title using selected provider fallback."""
    chain = []

    if settings.LLM_PROVIDER == "gemini":
        chain += [
            ("gemini-2.5", lambda: gemini.generate_title(text, "2.5")),
            ("gemini-1.5", lambda: gemini.generate_title(text, "1.5")),
        ]

    if settings.OPENAI_API_KEY:
        chain += [
            ("openai-4o-mini", lambda: openai.generate_title(text, "4o-mini")),
            ("openai-4.1-mini", lambda: openai.generate_title(text, "4.1-mini")),
            ("openai-o3-mini", lambda: openai.generate_title(text, "o3-mini")),
        ]

    result, _ = await fallback_chain(chain)
    return result
