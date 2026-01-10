# Fraud Detection MLOps System
# Multi-stage build for production deployment

# Stage 1: Base image with Python
FROM python:3.10-slim as base

# Set working directory
WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Dependencies
FROM base as dependencies

# Copy requirements
COPY requirements-prod.txt .

# Install Python dependencies (use pre-built wheels, no compilation)
RUN pip install --no-cache-dir --prefer-binary -r requirements-prod.txt

# Stage 3: Application
FROM dependencies as application

# Copy application code
COPY api/ ./api/
COPY monitoring/ ./monitoring/
COPY pipelines/ ./pipelines/
COPY config/ ./config/

# Create necessary directories
RUN mkdir -p logs models

# Copy model files (they should exist after running training)
COPY models/ ./models/

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
