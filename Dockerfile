# Multi-stage build for Railway optimization
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY setup.py README.md ./
COPY goldenverba/ ./goldenverba/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir .

# Production stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . /app/

# Create data directory and set permissions
RUN mkdir -p /app/data && chmod 755 /app/data

# Use PORT environment variable from Railway
EXPOSE ${PORT:-8000}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/ || exit 1

# Use Railway's PORT environment variable
CMD verba start --port ${PORT:-8000} --host 0.0.0.0
