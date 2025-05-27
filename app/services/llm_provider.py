from app.services import gemini
from fastapi import HTTPException


async def summarize(text: str, length: str = "short") -> dict:
    """
    Summarizes text using a fallback chain of LLM providers.

    Args:
        text (str): The content to summarize.
        length (str): 'short' or 'long' summary output.

    Returns:
        dict: A structured response with summary and provider info.
    """

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


async def rewrite(text: str, style: str = "simple") -> dict:
    """
    Rewrites text using the specified style. Falls back across Gemini 2.5 and 1.5.

    Args:
        text (str): The original text to rewrite.
        style (str): The desired style, either 'simple' or 'formal'.

    Returns:
        dict: A structured response with the rewritten text and provider info.
    """
    fallback_chain = [
        ("gemini-2.5", lambda: gemini.rewrite(text, style, variant="2.5")),
        ("gemini-1.5", lambda: gemini.rewrite(text, style, variant="1.5")),
    ]

    for provider, fn in fallback_chain:
        try:
            result = await fn()
            return {
                "rewritten": result,
                "provider": provider,
                "fallback_used": provider != fallback_chain[0][0],
            }
        except Exception:
            continue

    raise HTTPException(status_code=503, detail="All providers failed")
