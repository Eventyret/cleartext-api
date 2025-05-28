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

### Prerequisites

- **Python 3.13+**
- **uv** - Fast Python package installer ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

### Installation

**Unix/Linux/macOS:**

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Windows (Command Prompt):**

```cmd
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```

**Windows (PowerShell):**

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

**⚠️ IMPORTANT: Configure environment variables before running the application**

Copy the environment template and configure your API keys:

**Unix/Linux/macOS:**

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

**Windows:**

```cmd
copy .env.example .env
# Edit .env with your actual API keys using notepad or your preferred editor
```

### Running the Application

**All platforms:**

```bash
make run
```

**Alternative (if make is not available on Windows):**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Development Commands

The project includes a Makefile with common development tasks:

| Command        | Description                                         | Windows Alternative                                                                    |
| -------------- | --------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `make install` | Set up virtual environment and install dependencies | See Installation section above                                                         |
| `make run`     | Start the development server                        | `uvicorn app.main:app --reload`                                                        |
| `make test`    | Run the test suite                                  | `set PYTHONPATH=. && pytest -v` (CMD) or `$env:PYTHONPATH="."; pytest -v` (PowerShell) |
| `make lint`    | Run code linting                                    | `ruff check .`                                                                         |
| `make format`  | Format code                                         | `ruff format .`                                                                        |

**Note for Windows users:** If you don't have `make` installed, you can install it via:

- **Chocolatey**: `choco install make`
- **Scoop**: `scoop install make`
- Or use the individual commands listed in the table above

## 🔐 Environment Variables

**The application will crash on startup if these environment variables are not properly configured.**

The application requires the following environment variables:

| Variable           | Required | Description                                 | Example          |
| ------------------ | -------- | ------------------------------------------- | ---------------- |
| `INTERNAL_API_KEY` | ✅       | Internal API key for endpoint security      | `supersecure123` |
| `LLM_PROVIDER`     | ✅       | Primary LLM provider (`gemini` or `openai`) | `gemini`         |
| `GEMINI_API_KEY`   | ✅\*     | Google Gemini API key                       | `AIzaSy...`      |
| `OPENAI_API_KEY`   | ✅\*     | OpenAI API key                              | `sk-proj-...`    |
| `ENV`              | ❌       | Environment mode                            | `development`    |

\*Required based on selected `LLM_PROVIDER`

### 🔄 LLM Provider Fallback Behavior

The application implements intelligent fallback across LLM providers:

1. **Primary Provider**: The `LLM_PROVIDER` setting determines which provider to try first

   - `LLM_PROVIDER=gemini`: Tries Gemini 2.5 → Gemini 1.5 first
   - `LLM_PROVIDER=openai`: Tries OpenAI models first

2. **Cross-Provider Fallback**: If you provide **both** API keys, the system will fallback across providers:

   - With both keys: Primary provider models → Secondary provider models
   - With one key: Only uses that provider's models

3. **Example Configurations**:

   ```bash
   # Gemini primary with OpenAI fallback
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your-gemini-key
   OPENAI_API_KEY=your-openai-key

   # OpenAI only
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your-openai-key

   # Gemini only
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your-gemini-key
   ```

**💡 Recommendation**: Provide both API keys for maximum reliability and automatic failover.

## 🐳 Docker Support

**⚠️ CRITICAL: Environment variables must be provided to Docker containers**

### Production

Minimal, secure, multistage Alpine build using a non-root user:

```bash
# Build the image
docker build -t cleartext-api .

# Run with environment variables from .env file
docker run --env-file .env -p 8000:8000 cleartext-api

# Or pass environment variables directly
docker run \
  -e INTERNAL_API_KEY="your-secure-key" \
  -e GEMINI_API_KEY="your-gemini-key" \
  -e LLM_PROVIDER="gemini" \
  -p 8000:8000 \
  cleartext-api
```

### Development

Includes hot reload via `--reload` for local iteration:

```bash
# Build development image
docker build -f Dockerfile.dev -t cleartext-api-dev .

# Run with environment file
docker run --env-file .env -p 8000:8000 cleartext-api-dev
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
