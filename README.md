# Cleartext API

A small, high-performance API built with FastAPI for language-related tasks like summarization, rewriting, and language detection. The goal is to provide a secure, async-first, and extensible service that interacts with a large language model (Google Gemini) in a clean and scalable way.

---

## 🚧 Work In Progress

This project is being developed as part of a backend coding test. It reflects best practices around structure, security, and maintainability — while staying within a focused scope.

---

## ✅ Goals

- [x] Async FastAPI app with strong typing
- [x] OpenAPI documentation via `/docs`
- [x] Environment-based configuration with `.env`
- [x] Rate limiting and basic security measures
- [ ] Endpoints for:
  - [x] `/summarize`
  - [x] `/rewrite`
  - [ ] `/title`
  - [ ] `/language-detect`
- [ ] Unit tests for endpoints
- [ ] Dockerfile for deployment
- [ ] Reflection of tech choices

---

## 📦 Stack

- FastAPI (async + type-safe)
- Python 3.11
- Google Generative AI (Gemini)
- `langdetect` for language classification
- `slowapi` for rate limiting
- `uv` for fast dependency and virtualenv management

---

## 🔧 Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## 🧪 Example Usage

### `POST /summarize`

Request:

```json
{
  "text": "FastAPI is a modern Python framework for building APIs.",
  "length": "short"
}
```

### `POST /rewrite`

Request:

```json
{
  "text": "Could you please assist me with this?",
  "style": "simple"
}
```

The API is self-documented using FastAPI's built-in Swagger UI and ReDoc:

- [Swagger UI (interactive)](http://localhost:8000/docs)
- [ReDoc (minimal)](http://localhost:8000/redoc)

## 🔌 Available Endpoints

- `POST /summarize` — Generate a short or long summary
- `POST /rewrite` — Rewrite text in a simple or formal tone
- `POST /language-detect` — (Coming soon)
