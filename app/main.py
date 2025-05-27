from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from dotenv import load_dotenv

from app.api.router import api_router

load_dotenv()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Cleartext API",
    description="A language-processing API with summarization, rewriting, and language detection.",
    version="1.0.0",
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter
app.state.limiter = limiter

# API Router
app.include_router(api_router)
