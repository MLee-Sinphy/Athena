# ARCHITECTURE.md

> Arquitetura oficial validada pelo responsável em 2026-08-22. Cada incremento ainda depende do portão correspondente em `TESTS.md`.

## Visão geral

Aplicação web cliente-servidor: SPA React estática no GitHub Pages consome uma API REST Django por HTTPS. Django concentra autenticação, autorização e regras; PostgreSQL é a fonte transacional; mídia persiste no VPS por abstração de storage.

```text
Navegador -> GitHub Pages (React)
          -> HTTPS -> Open Library Covers (somente imagens por ISBN)
          -> HTTPS/CORS -> Reverse proxy -> Django/DRF -> PostgreSQL
                                               |-> diretório de mídia
                                               |-> backup externo criptografado
```

## Objetivos arquiteturais
- Integridade sob concorrência de reservas.
- Regras de domínio centralizadas e testáveis.
- Segurança entre origens distintas.
- Implantação e operação compreensíveis para estudo.
- Evolução de storage e hardware sem acoplar o domínio.

## Restrições arquiteturais
- Uma instituição por implantação.
- React com `HashRouter` no endereço padrão do GitHub Pages.
- Python, Django, DRF, PostgreSQL e Django ORM no backend.
- Backend sob demanda; frontend deve tolerar indisponibilidade.
- Token não persiste no navegador.

## Componentes principais

### Frontend React
#### Responsabilidade
Rotas, componentes, formulários, i18n, acessibilidade, estado de sessão em memória e consumo da API.
#### Entradas
Interações, preferência de idioma e respostas da API.
#### Saídas
Requisições HTTPS e interface visual.
#### Dependências
API publicada e arquivos estáticos do GitHub Pages.
#### Limites
Não decide autorização, prioridade ou disponibilidade definitiva.

### API Django/DRF
#### Responsabilidade
Autenticar, autorizar, validar contratos e orquestrar casos de uso.
#### Entradas
HTTP JSON e uploads validados.
#### Saídas
JSON, códigos HTTP, mídia autorizada e logs.
#### Dependências
Serviços de domínio, ORM, PostgreSQL e storage.
#### Limites
Não deve conter regra complexa dispersa em views ou serializers.

### Serviços de domínio
#### Responsabilidade
Calendário, disponibilidade, fila, concessão, retirada, devolução, penalidades, avaliações e auditoria.
#### Entradas
Comandos tipados e estado persistido.
#### Saídas
Resultados e eventos de domínio persistíveis.
#### Dependências
Repositórios/ORM dentro de transações explícitas.
#### Limites
Não dependem de React, filesystem concreto ou fornecedor de e-mail.

### PostgreSQL
#### Responsabilidade
Fonte de verdade relacional, constraints, transações e histórico.
#### Entradas
Consultas e migrações pelo ORM.
#### Saídas
Dados consistentes e bloqueios concorrentes.
#### Dependências
Volume persistente e rotina de backup.
#### Limites
Não armazena imagens binárias por padrão. WhatsApp é contato pessoal opcional em formato internacional; não representa consentimento para envio nem segundo fator ativo.

### Storage de mídia
#### Responsabilidade
Guardar capas e imagens por interface do Django Storage.
#### Entradas
Arquivos validados.
#### Saídas
Caminhos e streams.
#### Dependências
Diretório persistente no VPS na v1.
#### Limites
Regras de negócio não conhecem o caminho físico. Capas externas por ISBN não são copiadas para o banco ou volume: o frontend consulta diretamente a Open Library, com mídia local como fallback.

### Open Library
#### Responsabilidade
Fornecer, em baixo volume, metadados bibliográficos opcionais no seed e capas públicas por ISBN.
#### Limites
Não é fonte transacional nem requisito para login, catálogo ou circulação. O backend armazena somente metadados fundamentais e a URL de atribuição; o navegador carrega a imagem externa. Importações identificam o Athena, respeitam limite de requisições e mantêm fallback offline.

## Fluxos principais

### Login
React envia perfil escolhido, identificador (e-mail, matrícula ou WhatsApp) e senha; API limita tentativas, valida perfil, credencial e primeiro acesso, cria token opaco e devolve seu valor uma única vez. Backend guarda somente digest e metadados.

### Reserva concorrente
API abre transação, valida política e penalidades, consulta disponibilidade com bloqueio adequado, associa exemplar e confirma. Uma operação concorrente reavalia o estado e recebe conflito explicável.

### Retirada e devolução
Retirada transaciona a reserva para empréstimo e registra exemplar/hora. Devolução encerra empréstimo, atualiza exemplar, calcula atraso/oportunidade e cria avisos internos, sem depender de e-mail.

## Fluxo de dados
1. Frontend valida somente formato e envia comando.
2. API autentica, autoriza e valida o contrato.
3. Serviço aplica regras dentro de transação.
4. ORM persiste estado, histórico e auditoria.
5. API devolve representação apropriada ao perfil.
6. Frontend traduz resultado ou indisponibilidade.

## Estrutura de diretórios

```text
frontend/src/{app,components,features,i18n,services,styles,test}
backend/{config,apps,tests}
backend/apps/{accounts,catalog,circulation,policies,notifications,audit}
infra/{deploy,backup}
docs/
```

## Tecnologias

### React e TypeScript
- Finalidade: SPA tipada.
- Motivo da escolha: objetivo de estudo e contratos mais seguros.
- Alternativas consideradas: JavaScript puro, frameworks SSR.
- Limitações: GitHub Pages é estático; usar `HashRouter`.
- Versão mínima: definida e fixada no início da implementação após consulta às versões estáveis.

### Django e Django REST Framework
- Finalidade: API, autenticação, administração, ORM e migrações.
- Motivo da escolha: ecossistema maduro e familiaridade com Python.
- Alternativas consideradas: FastAPI, Node.js.
- Limitações: execução exige VPS, não hospedagem web estática.
- Versão mínima: linha estável suportada definida no início da implementação.

### PostgreSQL
- Finalidade: persistência transacional.
- Motivo da escolha: constraints, transações, índices, busca e concorrência robustas.
- Alternativas consideradas: SQLite apenas para protótipos, MySQL.
- Limitações: exige administração e backup.
- Versão mínima: linha suportada pelo ambiente de deploy.

## Dados

### Entidades principais
- `User`: perfil, matrícula, e-mail, credencial temporária e estado.
- `Title`: metadados, descrição e ISBN opcional.
- `Copy`: código, título, estado operacional.
- `Tag` e `TagSuggestion`: termo, título, autor e data.
- `LibraryCalendar`: semana regular e exceções.
- `PolicyVersion`: valores e vigência das regras.
- `Reservation`: leitor, título, exemplar, intervalo, prioridade e estado.
- `Loan`: reserva, exemplar, retirada, devolução prevista e real.
- `Penalty`: motivo, vigência e efeitos.
- `Rating`: empréstimo, notas opcionais e instante.
- `InternalNotice`: destinatário, tipo, leitura e resposta.
- `AuditEntry`: ator, ação, alvo, antes/depois, instante e justificativa.
- `AccessToken`: digest, usuário, atividade, expiração e revogação.

### Persistência
- Chaves substitutas e constraints de unicidade para matrícula, e-mail e código do exemplar.
- Horários em UTC; apresentação no fuso configurado da instituição.
- Eventos históricos preferem estado encerrado a exclusão.
- Médias e estatísticas são consultas ou projeções reconstruíveis, nunca fonte de verdade.

### Validação
- Banco garante invariantes estruturais; domínio garante regras temporais; API garante contrato.
- Busca considera texto da descrição e tags. Índices de busca serão definidos após medir o conjunto real.

### Migrações e compatibilidade
- Toda alteração de schema usa migração versionada, testada para avanço e restauração por backup.
- Migrações destrutivas exigem decisão e plano de dados.

## APIs
- REST JSON sob `/api/v1/`.
- Erros seguem formato estável com código, mensagem traduzível e detalhes seguros.
- Paginação em coleções; filtros e ordenação explicitamente permitidos.
- Idempotência em retirada/devolução e operações suscetíveis a repetição.
- OpenAPI gerada e validada como contrato.

## Integrações externas
- GitHub Pages, navegador e VPS na v1.
- Nenhum e-mail na v1.
- Storage futuro e hardware entram por interfaces, nunca acesso direto ao domínio.

## Segurança
- HTTPS obrigatório fora do desenvolvimento local.
- CORS somente para a origem exata publicada.
- Token aleatório de alta entropia, opaco, curto e revogável; digest no banco e valor somente na memória do React.
- Autorização no backend por perfil, propriedade e estado.
- Senhas pelo hasher do Django e política do `REQ-NF-002`.
- Rate limiting no login e endpoints sensíveis.
- Upload valida tipo, tamanho, nome e conteúdo; arquivos não executáveis.
- Segredos somente por configuração externa não versionada.

## Desempenho
- Paginação e seleção de campos evitam consultas ilimitadas.
- Índices em identificadores, estados, períodos, relações e busca medida.
- Evitar N+1 por carregamento relacionado explícito.
- Meta de carga definida em `REQ-NF-008`, sem prometer SLA não medido.

## Observabilidade
- Logs JSON com horário, nível, ambiente, request ID, ator pseudonimizado, ação e resultado.
- Métricas locais ou do VPS para erro, latência e recursos sem serviço pago obrigatório.
- Nunca registrar senha, token reutilizável ou conteúdo pessoal desnecessário.

## Estratégia de testes
- Unidades para domínio puro; integração real com PostgreSQL; contrato OpenAPI; componentes React; E2E; segurança e carga.
- Concorrência e restauração de backup exigem testes específicos.
- Detalhamento e portões em `TESTS.md`.

## Deploy e operação
- Frontend: build estático versionado e publicado pelo GitHub Pages.
- Backend: reverse proxy TLS, processo Django apropriado, PostgreSQL e volume de mídia persistente no VPS.
- Variáveis reais permanecem fora do Git.
- Healthcheck da API distingue processo disponível de dependências saudáveis.
- Backup consistente inclui `pg_dump` em formato custom e arquivo de mídia correspondente, manifesto/checksums, criptografia e cópia fora do VPS.
- Retenção inicial: 7 diárias e 4 semanais; criar antes de mudanças de infraestrutura e testar restauração antes de entrega relevante.

## Decisões relacionadas
DECISION-001 a DECISION-006 em `DECISIONS.md`.

## Riscos técnicos
- Condições de corrida em disponibilidade e fila.
- Inconsistência entre backup do banco e mídia.
- Operação de VPS autogerenciado.
- Sessão não persistente pode aumentar logins.

## Questões em aberto
- Versões exatas das dependências serão fixadas no início da implementação, após validação da documentação.
- Fuso horário da primeira instituição será configuração obrigatória de deploy.
