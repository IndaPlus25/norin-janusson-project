FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# hdbscan / scikit-learn need a C/C++ toolchain to build wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src ./src

WORKDIR /app/src

# Cloud Run injects $PORT (default 8080); uvicorn must bind to it
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
