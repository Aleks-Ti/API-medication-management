FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY tg_bot/requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY tg_bot/ ./tg_bot/

CMD ["python", "-m", "tg_bot.main"]
