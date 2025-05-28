"""App configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Typed settings for accessing environment variables."""

    ENV: str = os.getenv("ENV", "development")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini").lower()

    @property
    def docs_enabled(self) -> bool:
        """Flag to check if API docs should be enabled (dev only)."""
        return self.ENV == "development"


settings = Settings()
