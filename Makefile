.PHONY: app-destroy app-down app-logs app-stop app-up bootstrap check check-backend check-frontend db-down db-up demo-seed

PYTHON ?= .venv/bin/python
RUFF ?= .venv/bin/ruff

bootstrap:
	python3 -m venv .venv
	.venv/bin/pip install -r backend/requirements-dev.txt
	cd frontend && npm ci

db-up:
	docker compose up -d --wait postgres

db-down:
	docker compose down

app-up:
	docker compose up -d --build --wait

app-stop:
	docker compose stop

app-down:
	docker compose down

app-logs:
	docker compose logs --follow api postgres

demo-seed:
	@test -n "$(ATHENA_DEMO_PASSWORD)" || (echo "ATHENA_DEMO_PASSWORD is required" >&2; exit 2)
	docker compose exec -T -e ATHENA_DEMO_PASSWORD api python manage.py seed_demo_data --enrich-open-library

app-destroy:
	@ATHENA_DESTROY_CONFIRM="$(ATHENA_DESTROY_CONFIRM)" ./scripts/destroy_local.sh

check-backend:
	$(RUFF) format --check backend
	$(RUFF) check backend
	$(PYTHON) backend/manage.py makemigrations --check --dry-run
	$(PYTHON) backend/manage.py test accounts catalog circulation governance health

check-frontend:
	cd frontend && npm run lint
	cd frontend && npm run test
	cd frontend && npm run build

check: check-backend check-frontend
	./scripts/verify_bootstrap.sh
