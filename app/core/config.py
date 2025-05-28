"""App configuration loaded from environment variables."""

from typing import Optional
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed settings for accessing environment variables."""

    ENV: str = Field(default="development")
    GEMINI_API_KEY: Optional[str] = Field(default=None)
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    LLM_PROVIDER: str = Field(default="gemini")
    INTERNAL_API_KEY: str = Field(..., description="Required internal API key")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        extra="ignore",
    )

    @model_validator(mode="after")
    def check_llm_keys(self):
        """Ensure required LLM key is set based on selected provider."""
        if self.LLM_PROVIDER == "gemini" and not (self.GEMINI_API_KEY or "").strip():
            raise RuntimeError(
                "Missing GEMINI_API_KEY: You selected 'gemini' as the LLM provider but did not set the GEMINI_API_KEY in the environment."
            )
        if self.LLM_PROVIDER == "openai" and not (self.OPENAI_API_KEY or "").strip():
            raise RuntimeError(
                "Missing OPENAI_API_KEY: You selected 'openai' as the LLM provider but did not set the OPENAI_API_KEY in the environment."
            )
        return self

    @property
    def docs_enabled(self) -> bool:
        """Return True if docs should be enabled in this environment."""
        return self.ENV == "development"


settings = Settings()
