from fastapi import HTTPException
from app.core.config import settings
from app.services.llm import gemini, openai


async def fallback_chain(operations):
    for provider, fn in operations:
        try:
            return await fn(), provider
        except Exception:
            continue
    raise HTTPException(status_code=503, detail="All providers failed")


async def summarize(text: str, length: str = "short") -> dict:
    chain = []

    if settings.LLM_PROVIDER == "gemini":
        chain += [
            ("gemini-2.5", lambda: gemini.summarize(text, length, "2.5")),
            ("gemini-1.5", lambda: gemini.summarize(text, length, "1.5")),
        ]
    if settings.OPENAI_API_KEY:
        chain.append(("openai", lambda: openai.summarize(text, length)))

    result, provider = await fallback_chain(chain)
    return {"summary": result, "provider": provider}


async def rewrite(text: str, style: str = "simple") -> dict:
    chain = []

    if settings.LLM_PROVIDER == "gemini":
        chain += [
            ("gemini-2.5", lambda: gemini.rewrite(text, style, "2.5")),
            ("gemini-1.5", lambda: gemini.rewrite(text, style, "1.5")),
        ]
    if settings.OPENAI_API_KEY:
        chain.append(("openai", lambda: openai.rewrite(text, style)))

    result, provider = await fallback_chain(chain)
    return {"rewritten": result, "provider": provider}


async def generate_title(text: str) -> str:
    chain = []

    if settings.LLM_PROVIDER == "gemini":
        chain += [
            ("gemini-2.5", lambda: gemini.generate_title(text, "2.5")),
            ("gemini-1.5", lambda: gemini.generate_title(text, "1.5")),
        ]
    if settings.OPENAI_API_KEY:
        chain.append(("openai", lambda: openai.generate_title(text)))

    result, _ = await fallback_chain(chain)
    return result
