import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENV: str = os.getenv("ENV", "development")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    @property
    def docs_enabled(self) -> bool:
        return self.ENV == "development"


settings = Settings()
