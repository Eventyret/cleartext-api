"""Main application entry point for the Cleartext API."""

import asyncio
import logging
import random
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging

log_level = logging.DEBUG if settings.ENV == "development" else logging.INFO
setup_logging(level=log_level)


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Cleartext API",
    description="A language-processing API with summarization, rewriting, and language detection.",
    version="1.0.0",
    docs_url="/docs" if settings.docs_enabled else None,
    redoc_url="/redoc" if settings.docs_enabled else None,
    openapi_url="/openapi.json" if settings.docs_enabled else None,
)


@app.get("/", include_in_schema=False)
async def block_root():
    """Return a 404 plaintext response with anti-probe headers."""
    await asyncio.sleep(random.uniform(0.05, 0.2))  # Anti-probe jitter
    headers = {
        "X-Robots-Tag": "noindex, nofollow",
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
    }
    return PlainTextResponse("Not found", status_code=404, headers=headers)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.include_router(api_router)
