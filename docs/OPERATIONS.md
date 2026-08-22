# Operação e recuperação

## Observabilidade

A API escreve logs JSON em `stdout` com método, caminho, status, duração e UUID de correlação. O mesmo UUID retorna em `X-Request-ID`. Tokens, corpos, senhas e dados pessoais não são registrados. Os logs podem ser consultados com `docker compose -f compose.production.yaml logs api`.

## Docker sob demanda no servidor

```bash
make app-up
ATHENA_DEMO_PASSWORD='<senha forte mantida fora do Git>' make demo-seed
```

`app-up` constrói e inicia PostgreSQL e API, executa migrações e aguarda os healthchecks. O seed é idempotente, cria `mlee.admin@proton.me` (`ADM-001`), `mlee.student@proton.me` (`ALU-000001`), oito títulos reais e 25 exemplares; `--enrich-open-library` consulta metadados em baixo volume e as capas continuam externas.

- `make app-logs`: acompanha API e banco.
- `make app-stop`: para os contêineres, preservando contêineres e dados.
- `make app-down`: remove contêineres e rede, preservando os volumes.
- `make app-up`: recria e retoma usando os mesmos dados.
- `ATHENA_DESTROY_CONFIRM=destroy-athena-data make app-destroy`: remove contêineres, rede e volumes; apaga definitivamente banco e mídia local.

Não use `app-destroy` para apenas economizar recursos; `app-stop` ou `app-down` são suficientes. A senha demonstrativa é uma configuração do ambiente e nunca deve ser versionada.

## Backup

`scripts/backup.sh DIRETORIO` produz um pacote AES-256-CBC criptografado contendo dump PostgreSQL, mídia e checksums SHA-256. A senha vem somente de `ATHENA_BACKUP_PASSPHRASE`. Execuções diárias retêm sete dias; a execução de domingo é semanal e fica quatro semanas. O diretório deve ser sincronizado para armazenamento criptografado fora do VPS.

Exemplo:

```bash
export ATHENA_BACKUP_PASSPHRASE='valor mantido no cofre operacional'
./scripts/backup.sh /caminho/explicito/backup
```

As variáveis `POSTGRES_USER` e `POSTGRES_DB` exportadas no shell devem corresponder ao `.env.production` quando os valores padrão forem alterados.

## Restauração

A restauração substitui o banco e a mídia atuais. Faça-a apenas em ambiente isolado ou após confirmar a interrupção do serviço:

```bash
export ATHENA_BACKUP_PASSPHRASE='valor mantido no cofre operacional'
export ATHENA_RESTORE_CONFIRM=restore-athena
./scripts/restore_backup.sh /caminho/explicito/athena-daily-DATA.tar.gz.enc
```

O script valida os checksums antes de alterar os volumes. Após restaurar, execute a regressão e compare contagens e arquivos de amostra. O ensaio no VPS permanece obrigatório antes da entrega.
