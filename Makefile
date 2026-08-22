.PHONY: bootstrap check check-backend check-frontend db-down db-up

bootstrap:
	python3 -m venv .venv
	.venv/bin/pip install -r backend/requirements-dev.txt
	cd frontend && npm ci

db-up:
	docker compose up -d --wait postgres

db-down:
	docker compose down

check-backend:
	.venv/bin/ruff format --check backend
	.venv/bin/ruff check backend
	.venv/bin/python backend/manage.py makemigrations --check --dry-run
	.venv/bin/python backend/manage.py test

check-frontend:
	cd frontend && npm run lint
	cd frontend && npm run test
	cd frontend && npm run build

check: check-backend check-frontend
	./scripts/verify_bootstrap.sh
