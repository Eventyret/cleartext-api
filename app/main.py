from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import Settings

load_dotenv()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Cleartext API",
    description="A language-processing API with summarization, rewriting, and language detection.",
    version="1.0.0",
    docs_url="/docs" if Settings.docs_enabled else None,
    redoc_url="/redoc" if Settings.docs_enabled else None,
    openapi_url="/openapi.json" if Settings.docs_enabled else None,
)


@app.get("/", include_in_schema=False)
def block_root():
    return PlainTextResponse("Not found", status_code=404)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.include_router(api_router)
