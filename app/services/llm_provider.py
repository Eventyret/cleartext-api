"""LLM provider orchestrator with fallback across providers."""

import logging
from fastapi import HTTPException
from app.core.config import settings
from app.services.llm import gemini, openai

logger = logging.getLogger(__name__)


async def fallback_chain(operations):
    """Attempt multiple providers in order, returning the first successful result.

    Args:
        operations (list[tuple[str, Callable[[], Awaitable]]]): List of (provider_name, async function)

    Returns:
        tuple: A tuple of (result, provider_name) from the first successful provider.

    Raises:
        HTTPException: If all providers fail.
    """
    for provider, fn in operations:
        try:
            logger.debug("Trying provider: %s", provider)
            return await fn(), provider
        except Exception as e:
            logger.warning("Provider %s failed: %s", provider, str(e))
            continue

    logger.error("All providers failed during fallback chain")
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
    logger.info("Summarization handled by provider: %s", provider)
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
    logger.info("Rewrite handled by provider: %s", provider)
    return {"rewritten": result, "provider": provider}


async def generate_title(text: str) -> str:
    """Generate a title using selected provider fallback."""
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

    result, provider = await fallback_chain(chain)
    logger.info("Title generated using provider: %s", provider)
    return result
