from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed settings for accessing environment variables."""

    ENV: str = Field(default="development")
    GEMINI_API_KEY: str = Field(default="")
    OPENAI_API_KEY: str = Field(default="")
    LLM_PROVIDER: str = Field(default="gemini")
    INTERNAL_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",  # Allow exact match of variable names
        extra="ignore",
    )

    @property
    def docs_enabled(self) -> bool:
        return self.ENV == "development"


settings = Settings()
