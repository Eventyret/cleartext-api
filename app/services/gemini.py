import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)


async def summarize(text: str, length: str = "short", variant: str = "2.5") -> str:
    model_id = {
        "2.5": "models/gemini-2.5-flash-preview-05-20",
        "1.5": "models/gemini-1.5-flash",
    }.get(variant, "models/gemini-1.5-flash")

    model = genai.GenerativeModel(model_id)
    prompt = f"Summarize in a {length} way:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()
