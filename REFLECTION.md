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

All endpoints require a valid `x-api-key`, which acts as internal security. While this wouldn't be the only layer in production, it simulates how you might gate LLM-powered services where requests are usage-billed.

## 🤖 Language Model Selection & Fallback Strategy

I used **Google Gemini Flash** as the default provider over OpenAI's GPT models for several reasons:

- Flash is optimized for latency and cost, making it ideal for real-time endpoints
- It has a more generous free tier, which helps during prototyping
- It allowed me to explore fallback chaining across multiple Gemini models

However, the system is designed with **intelligent multi-provider fallback**:

### Fallback Architecture

1. **Primary Provider Selection**: The `LLM_PROVIDER` environment variable determines which provider to try first
2. **Model Progression**: Within each provider, it tries newer/better models first (e.g., Gemini 2.5 → 1.5)
3. **Cross-Provider Fallback**: If both API keys are provided, it falls back across providers for maximum reliability

### Example Fallback Chains

```python
# With LLM_PROVIDER=gemini and both keys:
Gemini 2.5 → Gemini 1.5 → OpenAI 4o-mini → OpenAI 4.1-mini → OpenAI o3-mini

# With LLM_PROVIDER=openai and both keys:
OpenAI 4o-mini → OpenAI 4.1-mini → OpenAI o3-mini → Gemini 2.5 → Gemini 1.5

# With LLM_PROVIDER=openai and only OpenAI key:
OpenAI 4o-mini → OpenAI 4.1-mini → OpenAI o3-mini

# With LLM_PROVIDER=gemini and only Gemini key:
Gemini 2.5 → Gemini 1.5
```

This design provides several benefits:

- **Reliability**: Automatic failover if one provider is down
- **Cost Optimization**: Can prioritize cheaper models first
- **Performance**: Can prioritize faster models for latency-sensitive operations
- **Flexibility**: Easy to change primary provider without code changes
- **Respect User Choice**: If a user only provides one API key, the system respects that choice and doesn't attempt unauthorized providers

Additionally, for lightweight use cases or more localized inference, **Gemini Nano** could be a solid alternative. It's optimized for smaller models and faster response times, which would be ideal for endpoints like language detection or short summaries where lower latency matters more than raw capability. In a scaled production environment, Nano could also help reduce cost and infrastructure demands significantly.

## 🚀 Performance & Scalability Considerations

### Caching Strategy

The current implementation processes every request fresh, which is inefficient for repeated inputs. A production system would benefit from multiple caching layers:

**1. Response Caching**

```python
# Redis-based caching for identical requests
cache_key = f"summarize:{hash(text)}:{length}"
cached_result = await redis.get(cache_key)
if cached_result:
    return json.loads(cached_result)
```

**2. Semantic Caching**

- Use embedding similarity to find "close enough" previous requests
- Cache responses for semantically similar inputs (e.g., "Hello world" vs "Hi world")
- Implement cache invalidation based on time or confidence thresholds

**3. Multi-Level Caching**

- **L1**: In-memory cache for hot requests (LRU with size limits)
- **L2**: Redis for shared cache across instances
- **L3**: Database for long-term storage of popular request patterns

### Background Processing

For production workloads, synchronous LLM calls can be problematic:

**1. Task Queues**

```python
# Celery/RQ for heavy processing
@celery.task
async def process_large_document(document_id, user_id):
    # Process in background, notify via webhook/websocket
    pass
```

**2. Streaming Responses**

```python
# FastAPI streaming for real-time feedback
async def stream_summary(text: str):
    async for chunk in llm_provider.stream_summarize(text):
        yield f"data: {json.dumps(chunk)}\n\n"
```

**3. Batch Processing**

- Queue multiple requests for batch processing
- Optimize LLM calls by batching similar operations
- Implement priority queues for different user tiers

### Monitoring & Observability

Production LLM services need comprehensive monitoring:

- **Cost Monitoring**: Token usage and API costs per endpoint
- **Cache Hit Rates**: Effectiveness of caching strategies
- **Provider Health**: Success rates and fallback frequency
- **User Analytics**: Most common request patterns for cache optimization

## 🐳 Deployment & Environment Management

### Current State

The application uses environment variables for configuration, which is a good practice for the [12-factor app methodology](https://12factor.net/config). However, the initial Docker setup had a critical gap: **it didn't document how to pass environment variables to containers**.

The app requires several environment variables:

- `INTERNAL_API_KEY` - for endpoint security
- `GEMINI_API_KEY` or `OPENAI_API_KEY` - for LLM provider access
- `LLM_PROVIDER` - to select which LLM service to use

Without these, the container crashes on startup with a Pydantic validation error, which is exactly what happened in testing.

### Production Deployment Considerations

For production deployment, I would implement a more robust secrets management strategy:

**1. Secrets Management**

- **AWS**: Use AWS Secrets Manager or Parameter Store with IAM roles
- **Azure**: Azure Key Vault with managed identities
- **GCP**: Secret Manager with service account authentication
- **Kubernetes**: Native secrets with RBAC and encryption at rest

**2. Container Orchestration**

```yaml
# Example Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cleartext-api
spec:
  template:
    spec:
      containers:
        - name: api
          image: cleartext-api:latest
          env:
            - name: INTERNAL_API_KEY
              valueFrom:
                secretKeyRef:
                  name: cleartext-secrets
                  key: internal-api-key
            - name: GEMINI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: cleartext-secrets
                  key: gemini-api-key
```

**3. CI/CD Pipeline Integration**

- Secrets injected at deployment time, never stored in code
- Different secret stores for staging vs production
- Automated secret rotation capabilities
- Audit logging for secret access

**4. Runtime Security**

- Use distroless or minimal base images
- Run containers as non-root users (already implemented)
- Network policies to restrict egress to only required LLM APIs
- Resource limits and health checks

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
- **Implement proper secrets management** (used simple environment variables instead)
- **Add comprehensive deployment documentation** (initially missed Docker env var requirements)

These were conscious tradeoffs to focus on clarity, robustness, and test coverage first.

## 🚀 What I'd Do Next

If this project were going into production, I'd prioritise:

**Immediate (Security & Deployment)**

- Implement proper secrets management (AWS Secrets Manager, Azure Key Vault, etc.)
- Add comprehensive deployment documentation with environment variable handling
- Switch to distroless Docker images for better security
- Add health checks and graceful shutdown handling
- Implement proper logging with structured output (JSON) for observability

**Short-term (Performance & Caching)**

- **Basic response caching** for identical requests (Redis or in-memory)
- **Streaming support** for real-time user feedback during processing
- **Background task queues** (Celery/RQ) for large document processing
- **Request deduplication** to avoid duplicate LLM calls

**Medium-term (Features & Reliability)**

- Normalising LLM responses to a consistent contract
- **Batch processing** for multiple requests to optimize LLM API usage
- Supporting usage metering and rate-based billing
- Expanding the frontend UI to support visual feedback per operation
- **Circuit breakers** for LLM provider failures with exponential backoff
- **Preferred Model Selection**: Add `PREFERRED_MODEL` environment variable to allow users to specify exact models (e.g., `openai-4o-mini`, `gemini-1.5`) while maintaining fallback chains. This would be a valuable addition that gives users fine-grained control while keeping the robust fallback system as a safety net.

**Long-term (Scale & Operations)**

- **Advanced monitoring**: Token usage tracking, cost analytics, cache hit rates
- **Auto-scaling** based on queue depth and response times
- **A/B testing framework** for different LLM models and prompts
- Setting up automated testing in staging environments that mirror production
- **Intelligent request routing** based on content type and user tier

### Performance Impact Estimates

Based on typical API patterns:

- **Basic caching**: Significant latency reduction for repeated requests
- **Background processing**: Eliminates user wait time for large documents
- **Streaming**: Perceived performance improvement of 3-5x for long responses
- **Request deduplication**: Reduces unnecessary LLM API costs

## ✅ Summary

This project shows how I approach building backend services:

- Type-safe, async-first, and well-documented
- Secure by default, with clear logs and fallback safety
- Modular and test-driven with room to grow

The initial Docker deployment gap highlighted an important lesson: **configuration and deployment documentation is as critical as the code itself**. In production, I would prioritize secrets management and deployment automation from day one, not as an afterthought.

Given more time, I'd turn this into a production-ready service with all the security, observability, and operational features needed for real clients.
