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

wstart:
	uv run uvicorn \
		--host $$HOST \
		--port $$PORT \
		"$$APP_MODULE" \
		--workers 4

dac:
	docker compose down && docker compose up -d

revision:
	uv run alembic revision --autogenerate -m "$(RUN_ARGS)"

migrate:
	uv run alembic upgrade head

st:
	ruff . --fix
