FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src:$PYTHONPATH

COPY pyproject.toml README.md ./
COPY src ./src
COPY docs ./docs

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

CMD ["sh", "-c", "uvicorn ai_feed_mcp.http_app:app --host 0.0.0.0 --port ${MCP_SERVER_PORT:-8081}"]

