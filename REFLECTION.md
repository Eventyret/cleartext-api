# Reflection

This project was built as part of a backend coding test, with a focus on designing a real-world-ready, secure, and maintainable REST API using FastAPI and a language model (LLM) backend. My goal was to keep the scope focused but still demonstrate a solid architecture, reasonable fallback logic, and best practices across the stack.

## 🔧 Design Choices

I chose **FastAPI** for several reasons:

- Built-in async support with great performance out of the box
- Automatic OpenAPI documentation with zero extra effort
- Strong typing with Pydantic for input validation
- Clean developer experience for quick iteration

Compared to alternatives like Flask, FastAPI offers better native async handling and eliminates the need for external libraries for things like request validation or schema generation.

The project is designed around a small but modular architecture:

- Each endpoint is separated into its own file for clarity and testability
- Business logic is abstracted into services (e.g., `llm_provider.py`)
- Configuration is environment-based with a `.env` file pattern

All endpoints require a valid `x-api-key`, which acts as internal security. While this wouldn’t be the only layer in production, it simulates how you might gate LLM-powered services where requests are usage-billed.

## 🤖 Language Model Selection

I used **Google Gemini Flash** over OpenAI’s GPT models for a few reasons:

- Flash is optimized for latency and cost, making it ideal for real-time endpoints
- It has a more generous free tier, which helps during prototyping
- It allowed me to explore fallback chaining across multiple Gemini models (if needed)

That said, OpenAI would still be a strong option depending on the feature needs (e.g., function calling, embeddings). For now, Gemini Flash offered a good tradeoff between speed, availability, and pricing.

Additionally, for lightweight use cases or more localized inference, **Gemini Nano** could be a solid alternative. It's optimized for smaller models and faster response times, which would be ideal for endpoints like language detection or short summaries where lower latency matters more than raw capability. In a scaled production environment, Nano could also help reduce cost and infrastructure demands significantly.

## 🧪 Testing Strategy

I wrote 17 automated tests that cover all endpoints and the fallback behavior of the LLM provider service. These include:

- Input validation (empty strings, invalid fields)
- Logical branching (e.g., fallback when provider fails)
- Integration-level API testing with expected outputs

Tests are run via `make test` and use standard `pytest`. CI also checks formatting, linting, and docstring coverage.

## 📉 What I Scoped Out

With limited time (6–8 hours), I chose not to:

- Implement output normalization across LLMs (e.g., force all responses to Markdown or plain text)
- Add usage-based metering or billing logic
- Enable streaming support for endpoints (though FastAPI would support it)
- Apply distroless Docker hardening or cloud deployment automation

These were conscious tradeoffs to focus on clarity, robustness, and test coverage first.

## 🚀 What I’d Do Next

If this project were going into production, I’d prioritise:

- Normalising LLM responses to a consistent contract
- Introducing in-memory or Redis caching for repeated inputs
- Switching to a distroless Docker image for better security
- Adding streaming support for real-time UIs
- Supporting usage metering and rate-based billing
- Expanding the frontend UI to support visual feedback per operation
- Moving model execution into a task queue for large workloads

## ✅ Summary

This project shows how I approach building backend services:

- Type-safe, async-first, and well-documented
- Secure by default, with clear logs and fallback safety
- Modular and test-driven with room to grow

Given more time, I'd turn this into a production-ready service with all the features and polish needed for real clients.
