"""Security utilities for internal API protection."""

from fastapi import Header, HTTPException, status
from app.core.config import settings


def verify_internal_api_key(x_api_key: str = Header(default=None, alias="x-api-key")):
    """Dependency to verify requests contain a valid internal API key.

    Args:
        x_api_key (str): The API key from the `x-api-key` header.

    Raises:
        HTTPException: If the API key is missing or invalid.

    Returns:
        None: Allows the request to proceed if the key is valid.
    """
    if x_api_key is None or x_api_key != settings.INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
