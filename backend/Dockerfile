# ─── Stage 1: Build ────────────────────────────────────────────
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ─── Stage 2: App ──────────────────────────────────────────────
# Copy app source code
COPY . .

# Create directory for SQLite database persistence
RUN mkdir -p /app/data

# Expose the port Render will assign via $PORT env var
EXPOSE 8000

# Start the FastAPI app
# Render injects $PORT automatically — we default to 8000 locally
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
