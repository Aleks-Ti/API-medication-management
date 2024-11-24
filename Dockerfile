FROM python:3.12-slim


WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv
RUN uv sync

COPY alembic.ini .
COPY ./migrations ./migrations
COPY ./scripts ./scripts.
COPY ./src ./src

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8333"]
