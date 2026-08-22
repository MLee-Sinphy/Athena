# Athena

Sistema web de estudo para empréstimo gratuito de livros físicos, com React, Django REST Framework e PostgreSQL.

## Requisitos locais

- Python 3.12+
- Node.js 22+
- Docker com Compose

## Preparação

```bash
make bootstrap
cp .env.example .env
make db-up
```

## Verificações

Com o PostgreSQL ativo:

```bash
make check
```

O comando executa formatação e lint do Python, valida migrações, roda os testes Django, lint e testes do React, gera o build e verifica a estrutura do bootstrap.

## Desenvolvimento

### Aplicação completa em Docker

```bash
make app-up
ATHENA_DEMO_PASSWORD='<senha forte escolhida>' make demo-seed
```

A API fica em `http://localhost:8000`. Use `make app-stop` para pausar preservando tudo, `make app-down` para remover os contêineres preservando os volumes e consulte `docs/OPERATIONS.md` antes de destruir dados.

Backend:

```bash
.venv/bin/python backend/manage.py migrate
.venv/bin/python backend/manage.py runserver
```

Frontend, em outro terminal:

```bash
cd frontend
npm run dev
```

O healthcheck da API fica em `http://localhost:8000/api/v1/health/`.

## Documentação

- Direção do produto: [`docs/PROJECT.md`](docs/PROJECT.md)
- Arquitetura: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Requisitos: [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md)
- Tarefas e portões: [`docs/TASKS.md`](docs/TASKS.md) e [`docs/TESTS.md`](docs/TESTS.md)
