# Implantação

## Arquitetura da versão 1.0

- O frontend estático é publicado pelo workflow `pages.yml` no GitHub Pages, sob `/Athena/`.
- A variável de repositório `VITE_API_BASE_URL` deve conter a URL HTTPS pública da API.
- No VPS, Caddy termina HTTPS e encaminha requisições ao Gunicorn/Django.
- PostgreSQL e mídia usam volumes Docker distintos e persistentes.
- A imagem PostgreSQL 18 monta o volume em `/var/lib/postgresql`, conforme o layout versionado dessa geração da imagem.

## Preparação do VPS

1. Instalar Docker com Compose e apontar um domínio para o servidor.
2. Copiar `.env.production.example` para `.env.production`, substituir todos os valores de exemplo e restringir a leitura do arquivo.
3. Definir `CORS_ALLOWED_ORIGINS` como a origem exata do GitHub Pages.
4. Executar `docker compose -f compose.production.yaml up -d --build --wait`.
5. Verificar `https://DOMINIO/api/v1/health/` e confirmar o cabeçalho `X-Request-ID`.
6. Configurar no GitHub a variável `VITE_API_BASE_URL` e executar o workflow de Pages.

O arquivo real `.env.production` nunca deve ser versionado. O deploy público depende de domínio, VPS e variável do GitHub fornecidos pelo responsável.

## Reversão

Mantenha a imagem anterior identificada pelo SHA do commit. Para reverter, restaure a imagem anterior no Compose; se houve migração incompatível, restaure primeiro um backup validado conforme `OPERATIONS.md`.
