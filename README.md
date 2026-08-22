# Athena

Athena é um sistema web de estudo para administrar o empréstimo gratuito de livros físicos em escolas, universidades, bibliotecas públicas e instituições semelhantes. O projeto combina um catálogo simples para leitores com controle individual de exemplares, reservas futuras, circulação e políticas configuráveis para administradores.

Esta é a primeira demonstração funcional. A candidata à versão `1.0.0` está implementada e a demonstração operacional foi aprovada; a tag formal permanece pendente dos últimos ensaios manuais descritos em [`docs/TESTS.md`](docs/TESTS.md).

## Acesso à demonstração

- Frontend no GitHub Pages: <https://mlee-sinphy.github.io/Athena/>
- API quando o VPS estiver ativo: <https://athena.179-197-79-149.sslip.io/api/v1/health/>

O software pode ser acessado pelo link do GitHub Pages, mas suas funções não estarão sempre disponíveis. O frontend permanece publicado continuamente, enquanto o backend e o PostgreSQL são ligados no VPS apenas durante estudos e demonstrações para não consumirem recursos desnecessariamente. Quando o backend estiver desligado, a página continuará abrindo e apresentará a mensagem esperada de serviço temporariamente indisponível.

As credenciais demonstrativas não são versionadas. No servidor de estudo, elas ficam no arquivo privado `.env.demo`, protegido com permissão `600`. O seed cria um aluno e um administrador e permite autenticação por e-mail, matrícula ou telefone, sempre com senha e perfil compatível.

## Funcionalidades

### Leitor

- Login como aluno por e-mail, matrícula ou telefone opcional.
- Catálogo agrupado por título, sem expor códigos internos ou dados de outros leitores.
- Pesquisa por título, autor, categoria, descrição e tags como `#medieval`.
- Comparação de exemplares disponíveis pela conservação, de 1 a 5 estrelas.
- Reserva por intervalo de dias úteis, com disponibilidade futura e fila FIFO privada.
- Alteração e cancelamento antes da retirada, sujeitos às políticas vigentes.
- Renovação sem invadir reserva posterior e sem ultrapassar o prazo máximo.
- Acompanhamento de reservas, empréstimos, avisos e penalidades.
- Avaliação do título e do estado físico após a devolução, além de sugestão de tags.

### Administrador

- Login separado e autorização por perfil.
- Cadastro de leitores com matrícula, e-mail, telefone opcional e senha temporária.
- Gestão de títulos, exemplares identificados individualmente, imagens, estados e tags.
- Confirmação de retirada e devolução e intervenção administrativa nas operações.
- Configuração versionada de dias de funcionamento, prazos, limites, tolerância de retirada, cancelamentos e penalidades.
- Gestão de dias úteis e fechamentos específicos da instituição.
- Auditoria imutável das intervenções e histórico preparado para análises futuras.
- Escolha entre seis temas visuais tokenizados para a instituição.

### Experiência e operação

- Interface React responsiva a partir de 320 px, adequada a computador e celular.
- Português e inglês, com preferência persistente e seleção inicial por localidade.
- Seis paletas, incluindo uma opção translúcida inspirada em interfaces modernas.
- Estados de carregamento, vazio, erro, acesso negado e backend indisponível.
- HTTPS automático, CORS restrito, limitação de tentativas de login e tokens opacos armazenados por digest.
- Seed idempotente com oito títulos reais e 25 exemplares sintéticos.
- Metadados em baixo volume pela Open Library e capas carregadas diretamente pelo navegador por ISBN.

## Arquitetura

| Camada | Tecnologia | Responsabilidade |
|---|---|---|
| Frontend | React 19, TypeScript e Vite | Interface bilíngue, responsiva, perfis, catálogo e circulação |
| API | Python 3.12, Django 6.1 e Django REST Framework | Autenticação, regras de negócio, autorização e auditoria |
| Banco | PostgreSQL 18 | Usuários, acervo, reservas, empréstimos, políticas e histórico |
| Proxy HTTPS | Caddy | TLS automático e encaminhamento público para a API |
| Desenvolvimento | Docker Compose | Ambientes locais reproduzíveis |
| Publicação | GitHub Actions e GitHub Pages | CI e frontend estático |

O catálogo apresenta um único título ao leitor, mas mantém cada cópia como entidade própria. Disponibilidade e fila usam transações PostgreSQL para impedir sobreposição em concorrência. Imagens locais são opcionais; as capas demonstrativas externas não sobrecarregam o banco nem o VPS.

## Estrutura do repositório

```text
Athena/
├── backend/
│   ├── accounts/            # usuários, autenticação e autorização
│   ├── catalog/             # títulos, exemplares, tags e imagens
│   ├── circulation/         # reservas, filas, empréstimos e penalidades
│   ├── governance/          # políticas, auditoria e avaliações
│   └── config/              # configuração Django por ambiente
├── frontend/                # React, testes de componentes e E2E
├── deploy/                  # configuração do Caddy
├── docs/                    # documentação oficial
├── scripts/                 # bootstrap, backup, restauração e carga
├── compose.yaml             # ambiente local
└── compose.production.yaml  # API, PostgreSQL e HTTPS no VPS
```

## Requisitos locais

- Git.
- Python 3.12 ou superior.
- Node.js 22 ou superior e npm.
- Docker Engine com o plugin Docker Compose.
- Linux, macOS ou Windows com ambiente compatível com o `Makefile`.

## Início rápido com Docker

```bash
git clone git@github.com:MLee-Sinphy/Athena.git
cd Athena
cp .env.example .env
make app-up
```

A API ficará em `http://localhost:8000/api/v1` e o healthcheck em `http://localhost:8000/api/v1/health/`.

Para inserir os dados demonstrativos, escolha uma senha forte e mantenha-a fora do Git:

```bash
ATHENA_DEMO_PASSWORD='<senha forte>' make demo-seed
```

Execute o frontend em outro terminal:

```bash
cd frontend
npm ci
npm run dev
```

Abra o endereço apresentado pelo Vite, normalmente `http://localhost:5173`.

## Desenvolvimento sem a API em container

```bash
make bootstrap
cp .env.example .env
make db-up
.venv/bin/python backend/manage.py migrate
.venv/bin/python backend/manage.py runserver
```

Em outro terminal:

```bash
cd frontend
npm run dev
```

## Testes e portões de qualidade

Com o PostgreSQL local ativo, execute a regressão principal:

```bash
make check
```

O comando verifica formatação e lint do Python, migrações, testes Django, lint e testes React, build e estrutura do repositório. As jornadas de navegador são executadas separadamente:

```bash
cd frontend
npx playwright install chromium firefox webkit
npm run test:e2e
```

A CI também verifica a configuração de produção, restauração de backup criptografado, volume sintético e 500 clientes concorrentes. O desenvolvimento segue tarefas incrementais e GATEs rastreados em [`docs/TASKS.md`](docs/TASKS.md) e [`docs/TESTS.md`](docs/TESTS.md).

## Operação sob demanda

### Ambiente local

```bash
make app-stop   # para e preserva containers e dados
make app-up     # inicia ou recria preservando volumes
make app-down   # remove containers e rede, preservando volumes
make app-logs   # acompanha os logs
```

A remoção definitiva dos dados locais exige confirmação explícita:

```bash
ATHENA_DESTROY_CONFIRM=destroy-athena-data make app-destroy
```

### VPS com HTTPS

```bash
docker compose -f compose.production.yaml up -d --build
docker compose -f compose.production.yaml stop
docker compose -f compose.production.yaml down
```

`stop` é a opção indicada para economizar recursos e retomar rapidamente. `down` remove containers e rede, mas preserva os volumes. Não acrescente `--volumes` a menos que a destruição do banco e dos certificados seja realmente desejada.

As configurações reais ficam em `.env.production` e as contas demonstrativas em `.env.demo`; ambos são ignorados pelo Git. Consulte [`docs/OPERATIONS.md`](docs/OPERATIONS.md) para backup, restauração, logs e procedimentos completos.

## Segurança e privacidade

- Nenhum segredo, senha demonstrativa ou ambiente real deve ser versionado.
- O PostgreSQL de produção não expõe sua porta ao host público.
- A API usa HTTPS, HSTS, CORS restrito e cabeçalhos defensivos.
- Senhas são tratadas pelo hash e pelos validadores do Django.
- Tokens são opacos; somente o digest é persistido, com expiração por inatividade e limite absoluto.
- Respostas do leitor não revelam identidade ou posição nominal de outras pessoas.
- Códigos internos de exemplares são exclusivos da administração.
- Logs evitam corpos, tokens, senhas e dados pessoais.
- Números e dados do seed são sintéticos e destinados somente a testes.

Este é um projeto educacional. Antes de uso institucional real, são necessárias revisão jurídica de privacidade, gestão profissional de segredos, retenção, monitoramento, backup externo e avaliação de segurança independente.

## Documentação oficial

- [Visão e escopo](docs/PROJECT.md)
- [Requisitos e regras de negócio](docs/REQUIREMENTS.md)
- [Arquitetura](docs/ARCHITECTURE.md)
- [UX, responsividade, acessibilidade e temas](docs/UX_UI.md)
- [Decisões técnicas](docs/DECISIONS.md)
- [Tarefas e implementação](docs/TASKS.md)
- [Testes, suítes e GATEs](docs/TESTS.md)
- [Roadmap e versionamento](docs/ROADMAP.md)
- [Operação e recuperação](docs/OPERATIONS.md)
- [Deploy](docs/DEPLOYMENT.md)
- [Features futuras](docs/FEATURES.md)

## Estado e próximos passos

A demonstração operacional e o GATE-009 estão aprovados. A versão `1.0.0` ainda não recebeu tag porque o GATE-008 mantém pendentes ensaios manuais com tecnologias assistivas e provas finais de restauração/carga no próprio VPS. E-mail, recuperação autônoma de senha, leitor óptico e WhatsApp/2FA permanecem documentados como evoluções futuras.

## Licença

O repositório ainda não declara uma licença de distribuição. Até que uma licença seja escolhida e adicionada, não presuma permissão para reutilização pública do código.
