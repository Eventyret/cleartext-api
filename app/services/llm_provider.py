from app.services import gemini
from fastapi import HTTPException


async def summarize(text: str, length: str = "short") -> dict:
    fallback_chain = [
        ("gemini-2.5", lambda: gemini.summarize(text, length, variant="2.5")),
        ("gemini-1.5", lambda: gemini.summarize(text, length, variant="1.5")),
    ]

    for provider, fn in fallback_chain:
        try:
            result = await fn()
            return {
                "summary": result,
                "provider": provider,
                "fallback_used": provider != fallback_chain[0][0],
            }
        except Exception:
            continue

    raise HTTPException(status_code=503, detail="All providers failed")
