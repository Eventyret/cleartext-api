"""Security utilities for internal API protection."""

import logging
from fastapi import Header, HTTPException, status
from app.core.config import settings

logger = logging.getLogger(__name__)


def verify_internal_api_key(x_api_key: str = Header(default=None, alias="x-api-key")):
    """Verify requests contain a valid internal API key.

    Args:
        x_api_key (str): The API key from the `x-api-key` header.

    Raises:
        HTTPException: If the API key is missing or invalid.
    """
    if x_api_key is None or x_api_key != settings.INTERNAL_API_KEY:
        logger.warning("Unauthorized request: missing or invalid x-api-key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

    logger.info("Internal API key validated")
