ifeq (revision,$(firstword $(MAKECMDGOALS)))
	# use the rest as arguments for run
	RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
	# ... and turn them into do-nothing targets
	$(eval $(RUN_ARGS):;@:)
endif

.PHONY: start revision migrate

start:
	uv run uvicorn \
		--reload \
		--host $$HOST \
		--port $$PORT \
		"$$APP_MODULE"

revision:
	poetry run alembic revision --autogenerate -m "$(RUN_ARGS)"

migrate:
	poetry run alembic upgrade head

st:
	ruff . --fix

mqdb:
	docker compose down && docker compose up -d

redis:
	docker run --name redis -p 6379:6379 -d --rm redis --requirepass 123425

p_db:
	docker run --name=podvig_db \
	 			-e SSL_MODE='disable'\
				-e POSTGRES_USER=$$PG_USER\
				-e POSTGRES_PASSWORD=$$PG_PASSWORD\
				-e POSTGRES_DB=$$PG_DB\
				-e TZ=GMT-3\
				-p $$PG_PORT:5432 -d --rm postgres:alpine
