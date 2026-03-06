ifeq (revision,$(firstword $(MAKECMDGOALS)))
	# use the rest as arguments for run
	RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
	# ... and turn them into do-nothing targets
	$(eval $(RUN_ARGS):;@:)
endif

.PHONY: start start-bot up down bot-up bot-down infra-up infra-down revision migrate

# --- Локальный запуск ---

# Для разработки бота локально:
# 1. make bot-up        — поднять всё кроме бота
# 2. make start-bot     — запустить бот локально
start-bot:
	uv run python -m tg_bot.main

# Для разработки api локально:
# 1. make infra-up      — поднять инфраструктуру
# 2. make start         — запустить api локально
start:
	uv run uvicorn \
		--reload \
		--host $$HOST \
		--port $$PORT \
		"$$APP_MODULE"

wstart:
	uv run uvicorn \
		--host $$HOST \
		--port $$PORT \
		"$$APP_MODULE" \
		--workers 4

# --- Docker compose ---

# Поднять весь проект (все сервисы включая бот)
up:
	docker compose up -d

down:
	docker compose down

# Поднять всё кроме бота (для разработки бота локально)
bot-up:
	docker compose -f docker-compose.bot.yml up -d

bot-down:
	docker compose -f docker-compose.bot.yml down

# Поднять только инфраструктуру (для разработки api локально)
infra-up:
	docker compose -f docker-compose.infra.yml up -d

infra-down:
	docker compose -f docker-compose.infra.yml down

# --- Alembic ---

revision:
	uv run alembic revision --autogenerate -m "$(RUN_ARGS)"

migrate:
	uv run alembic upgrade head

# --- Lint ---

st:
	ruff . --fix
