# Cleartext API

A small, high-performance API built with FastAPI for language-related tasks like summarization, rewriting, and language detection. The goal is to provide a secure, async-first, and extensible service that interacts with a large language model (Google Gemini) in a clean and scalable way.

## ✅ Goals

- [x] Async FastAPI app with strong typing
- [x] OpenAPI documentation via `/docs`
- [x] Environment-based configuration with `.env`
- [x] Rate limiting and basic security measures
- [x] Dockerfile for deployment
- [ ] Unit tests for endpoints
- [ ] Reflection of tech choices
- [ ] `/title` endpoint (planned but scoped out for now)

## 📦 Stack

- FastAPI (async + type-safe)
- Python 3.11+
- Google Generative AI (Gemini)
- `langdetect` for language classification
- `slowapi` for rate limiting
- `uv` for dependency and virtualenv management

## 🔧 Local Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

To run locally:

```bash
make run
```

## 🐳 Docker Support

### Production

Minimal, secure, multistage Alpine build using a non-root user:

```bash
docker build -t clear-text-api .
docker run -p 8000:8000 clear-text-api
```

### Development

Includes hot reload support via `--reload`:

```bash
docker build -f Dockerfile.dev -t clear-text-api-dev .
docker run -p 8000:8000 clear-text-api-dev
```

## 🧪 Example Usage

### `POST /summarize`

```json
{
  "text": "FastAPI is a modern Python framework for building APIs.",
  "length": "short"
}
```

### `POST /rewrite`

```json
{
  "text": "Could you please assist me with this?",
  "style": "simple"
}
```

### `POST /language-detect`

```json
{
  "text": "Hola, ¿como estás?"
}
```

Response:

```json
{
  "language": "es"
}
```

## 🔐 Available Endpoints

- `POST /summarize` - Generate a short or long summary
- `POST /rewrite` - Rewrite text in a simple or formal tone
- `POST /language-detect` - Detect the language of a given text
- `POST /title` - _(Planned)_ Auto-generate a catchy title

## 🗺️ API Docs

Run locally and access:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
