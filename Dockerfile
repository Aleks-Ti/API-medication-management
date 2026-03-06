FROM python:3.12-slim


WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv
RUN uv sync

COPY alembic.ini .
COPY ./migrations ./migrations
COPY ./scripts ./scripts
COPY ./api_backend ./api_backend

CMD ["sh", "-c", "uv run uvicorn api_backend.main:app --host 0.0.0.0 --port ${PORT:-8001}"]
