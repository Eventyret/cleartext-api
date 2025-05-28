import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY
MODEL = "gpt-3.5-turbo"


async def summarize(text: str, length: str = "short") -> str:
    prompt = f"Summarize the following text in a {length} way:\n\n{text}"
    response = await openai.ChatCompletion.acreate(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


async def rewrite(text: str, style: str = "simple") -> str:
    prompt = f"Rewrite this text in a more {style} tone:\n\n{text}"
    response = await openai.ChatCompletion.acreate(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


async def generate_title(text: str) -> str:
    prompt = f"Create a short, engaging title for:\n\n{text}"
    response = await openai.ChatCompletion.acreate(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip().strip('"')
