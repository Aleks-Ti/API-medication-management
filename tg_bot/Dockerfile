FROM python:3.12-slim

WORKDIR /app

COPY tg_bot/pyproject.toml tg_bot/uv.lock ./
RUN pip install uv
RUN uv sync --no-dev

COPY tg_bot/ ./tg_bot/

CMD ["uv", "run", "python", "-m", "tg_bot.main"]
