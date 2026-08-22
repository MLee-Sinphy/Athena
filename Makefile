.PHONY: bootstrap check check-backend check-frontend db-down db-up

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

check-backend:
	$(RUFF) format --check backend
	$(RUFF) check backend
	$(PYTHON) backend/manage.py makemigrations --check --dry-run
	$(PYTHON) backend/manage.py test accounts catalog circulation health

check-frontend:
	cd frontend && npm run lint
	cd frontend && npm run test
	cd frontend && npm run build

check: check-backend check-frontend
	./scripts/verify_bootstrap.sh
