# Cleartext API

A small, high-performance API built with FastAPI for language-related tasks like summarization, rewriting, language detection, and title generation. The goal is to provide a secure, async-first, and extensible service that interacts with a large language model (Google Gemini) in a clean and scalable way.

## ✅ Goals

- [x] Async FastAPI app with strong typing and validation
- [x] OpenAPI documentation via `/docs`
- [x] Environment-based configuration via `.env`
- [x] Rate limiting and basic API key security
- [x] Dockerfile for production and development use
- [x] Unit and fallback logic tests (17 in total)
- [x] `/title` endpoint with LLM fallback
- [x] Reflection of design choices in `reflection.md`

## 📦 Tech Stack

- **FastAPI** - async-ready API framework with built-in OpenAPI docs
- **Python 3.13**
- **Google Generative AI (Gemini)** - LLM backend
- **Open AI** - LLM backend
- **langdetect** - language classification
- **slowapi** - simple rate limiting
- **uv** - dependency and virtualenv management
- **Docker** - multistage containerized setup

## 🔧 Local Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

To start the server:

```bash
make run
```

## 🐳 Docker Support

### Production

Minimal, secure, multistage Alpine build using a non-root user:

```bash
docker build -t cleartext-api .
docker run -p 8000:8000 cleartext-api
```

### Development

Includes hot reload via `--reload` for local iteration:

```bash
docker build -f Dockerfile.dev -t cleartext-api-dev .
docker run -p 8000:8000 cleartext-api-dev
```

## 🔐 Security

All endpoints are protected by an internal `x-api-key` header to simulate access control and usage protection. Unauthorized attempts are logged using per-module loggers.

## 📊 Endpoints

| Method | Route              | Description                           |
| ------ | ------------------ | ------------------------------------- |
| POST   | `/summarize`       | Generate a short or long summary      |
| POST   | `/rewrite`         | Rewrite text in simple or formal tone |
| POST   | `/language-detect` | Detect the language of a given input  |
| POST   | `/title`           | Generate a title using LLM fallback   |

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

## 🗺️ API Documentation

Auto-generated docs available at runtime:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🧪 Tests

Run the full test suite using:

```bash
make test
```

The suite includes coverage for:

- All endpoint paths and input validation
- LLM fallback chain behavior
- Edge cases like empty strings, invalid inputs, and exhausted providers

All 17 tests currently pass.

## 💬 Notes

- LLM response normalization is currently disabled (for speed), so outputs may vary (e.g., Markdown, plain text).
- Response speed (\~10s) may improve with caching or async queues in a production setup.
- Title generation uses fallback across multiple LLMs and exits on first success.

## 🧠 Reflection

The design choices, tradeoffs, and areas for future improvement are detailed in [`REFLECTION.md`](./REFLECTION.md).
