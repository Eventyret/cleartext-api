# ---- Builder ----
    FROM python:3.13.3-alpine AS builder
    WORKDIR /app
    
    # Install required build tools for wheels and native deps
    RUN apk add --no-cache gcc musl-dev libffi-dev
    
    COPY requirements.txt .
    RUN pip install --upgrade pip \
        && pip install --no-cache-dir --prefix=/install -r requirements.txt
    
    COPY . .
    
    # ---- Final Slim Alpine Image ----
    FROM python:3.13.3-alpine AS final
    WORKDIR /app
    
    # Install runtime libs needed by some Python packages
    RUN apk add --no-cache libffi
    
    COPY --from=builder /install /usr/local
    COPY --from=builder /app .
    
    # Create non-root user
    RUN adduser -D -H appuser
    USER appuser
    
    EXPOSE 8000
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    