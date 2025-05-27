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
    return _models.get(variant, _models["1.5"])


async def summarize(text: str, length: str = "short", variant: str = "2.5") -> str:
    model = get_model(variant)
    prompt = f"Summarize the following text in a {length} way:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()


async def rewrite(text: str, style: str = "simple", variant: str = "2.5") -> str:
    model = get_model(variant)
    prompt = f"Rewrite the following text in a more {style} tone:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()
