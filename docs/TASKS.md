# TASKS.md

> Plano executável aprovado em 2026-08-22. Cada tarefa só pode iniciar quando suas dependências e seu portão de entrada forem satisfeitos.

# TASK-001 — Inicializar frontend, backend e qualidade
## Estado
Concluída.
## Tipo
Chore.
## Prioridade
Alta.
## Origem
ROADMAP 0.1.0; ARCHITECTURE.
## Objetivo
Criar React/TypeScript, Django/DRF, PostgreSQL, ambientes, formatação, lint e CI mínimos.
## Escopo
### Incluído
Estrutura oficial, healthcheck, configuração segura, testes vazios executáveis.
### Não incluído
Domínio funcional.
## Dependências
Validação humana; versões estáveis verificadas; GATE-000.
## Fontes de verdade obrigatórias
ARCHITECTURE, STYLE, CONSTRAINTS.
## Testes e portões relacionados
GATE-000, TEST-001 a TEST-003.
## Critérios de conclusão
Builds, lint, testes e banco de teste executam localmente e em CI.
## Riscos
Versões ou ambiente incompatíveis.
## Resultado
React/TypeScript, Django/DRF, PostgreSQL, healthcheck, testes, lint, formatação, build, Compose e CI foram inicializados. A verificação estrutural falhou antes do bootstrap e passou depois da implementação.
## Evidências
- Commits: `255b3b9`, `ed1e646` e `ce688cb`.
- CI aprovada: execução `32583985955` no GitHub Actions.
- PostgreSQL 18 criou o banco de teste e executou o teste do healthcheck na CI.
- Frontend: lint, um teste de componente e build aprovados.
- Backend: Ruff, verificação de migrações e um teste de API aprovados.
## Referências
GATE-000; TEST-001, TEST-002 e TEST-003.

# TASK-002 — Implementar contas e autenticação
## Estado
Concluída — GATE-001 e GATE-002 aprovados.
## Tipo
Feature.
## Prioridade
Alta.
## Origem
UC-001; REQ-F-001 a REQ-F-003.
## Objetivo
Entregar perfis, cadastro administrativo, primeiro acesso, sessão e recuperação assistida.
## Escopo
### Incluído
Senha, token opaco, rate limit, autorização base, telas bilíngues.
### Não incluído
Recuperação por e-mail.
## Dependências
TASK-001; GATE-001.
## Fontes de verdade obrigatórias
REQUIREMENTS, DECISION-003, UX_UI.
## Testes e portões relacionados
GATE-001 e GATE-002; TEST-010 a TEST-014.
## Critérios de conclusão
UC-001 e indisponibilidade da API verificados.
## Riscos
Enumeração, token vazado ou autorização apenas visual.
## Resultado
Contas de leitor e administrador, login por identificador único, token opaco revogável, primeiro acesso, troca e redefinição de senha, logout, CORS restrito e tratamento visual da API indisponível foram implementados. O token permanece apenas em memória no frontend e a interface pública inicial permite alternar entre português e inglês.
## Evidências
- Falha inicial: importação de `UserRole` inexistente antes da implementação.
- Modelo customizado, perfis, unicidade, hash, primeiro acesso e política de senha cobertos por 7 testes.
- CI PostgreSQL aprovada na execução `32584631836` para o commit `0446d38`.
- Falhas iniciais do GATE-002: modelo `AccessToken`, rotas de autenticação e estado de indisponibilidade ainda inexistentes.
- Backend: 21 testes cobrem identidades, erro neutro, rate limit, digest do token, limites de 30 minutos/8 horas, revogação, autorização, cadastro e recuperação administrativa e CORS.
- Frontend: 3 testes cobrem disponibilidade, falha sem falso sucesso e login sem persistência do token; lint, tipos e build aprovados.
- CI PostgreSQL aprovada nas execuções `32594658408` e `32594901125`; implementação final no commit `1f38c2c`.

# TASK-003 — Implementar acervo e catálogo
## Estado
Concluída — GATE-003 aprovado.
## Tipo
Feature.
## Prioridade
Alta.
## Origem
UC-002, UC-008; ROADMAP 0.2.0.
## Objetivo
Gerenciar títulos/exemplares e entregar busca agrupada e comparação.
## Escopo
### Incluído
Mídia, estados, tags, busca, filtros e conservação.
### Não incluído
Circulação.
## Dependências
TASK-002; GATE-002.
## Fontes de verdade obrigatórias
REQ-F-004, REQ-F-005, REQ-F-016; DECISION-004.
## Testes e portões relacionados
GATE-003; TEST-020 a TEST-023.
## Critérios de conclusão
UC-002 e administração do acervo verificados nos dois perfis.
## Riscos
Licença de mídia, N+1 e busca inconsistente.
## Resultado
Catálogo agrupado por título, comparação de exemplares disponíveis, busca textual e por `#tag`, CRUD administrativo de títulos/exemplares, imagens adicionais e mídia autenticada foram implementados. ISBN e páginas permanecem opcionais; códigos internos ficam restritos às APIs administrativas.
## Evidências
- Falha inicial: importação de `catalog.models` inexistente antes da implementação.
- TEST-020 a TEST-023 cobertos por 11 testes específicos; regressão total de 32 testes de backend e 3 de frontend.
- Ruff, migrações, lint TypeScript e build aprovados.
- CI PostgreSQL aprovada na execução `32595446620` para o commit `ec803f7`.

# TASK-004 — Implementar calendário, políticas e disponibilidade
## Estado
Concluída — GATE-004 aprovado.
## Tipo
Feature.
## Prioridade
Alta.
## Origem
UC-003, UC-009.
## Objetivo
Calcular dias válidos, políticas versionadas e alocação sem sobreposição.
## Escopo
### Incluído
Calendário, prazos, limites, suspensão, transações e concorrência.
### Não incluído
Interface completa de circulação.
## Dependências
TASK-003; GATE-003.
## Fontes de verdade obrigatórias
RULE-005 a RULE-008, RULE-015.
## Testes e portões relacionados
GATE-004; TEST-030 a TEST-034.
## Critérios de conclusão
Disponibilidade e políticas passam testes de fronteira e concorrência.
## Riscos
Off-by-one e política retroativa.
## Resultado
Calendário semanal configurável, exceções de abertura/fechamento, políticas versionadas, limites e suspensão, penalidades, FIFO determinístico e alocação transacional sem sobreposição foram implementados.
## Evidências
- Falha inicial: módulo `circulation.models` inexistente antes da implementação.
- TEST-030 a TEST-034 cobertos por 13 testes de unidade, integração, autorização e concorrência.
- Teste concorrente executado no PostgreSQL real; exatamente uma das duas alocações simultâneas foi confirmada.
- Regressão de 45 testes de backend, lint e build do frontend aprovados na CI `32596027546` para `af1968d`.

# TASK-005 — Implementar circulação, fila e avisos
## Estado
Concluída — GATE-005 aprovado.
## Tipo
Feature.
## Prioridade
Alta.
## Origem
UC-003 a UC-006; ROADMAP 0.3.0.
## Objetivo
Entregar reserva, fila, retirada, devolução, alterações, penalidades e avisos internos.
## Escopo
### Incluído
Fluxos completos e intervenções administrativas.
### Não incluído
E-mail e hardware.
## Dependências
TASK-004; GATE-004.
## Fontes de verdade obrigatórias
REQ-F-006 a REQ-F-014; EXAMPLE-002 e EXAMPLE-003.
## Testes e portões relacionados
GATE-005; TEST-040 a TEST-047.
## Critérios de conclusão
Nenhum cenário concorrente sobrepõe exemplar; avisos e respostas são rastreáveis.
## Riscos
Corridas temporais e transições ambíguas.
## Resultado
Reserva automática, fila FIFO, retirada e devolução idempotentes, alteração, cancelamento, renovação, penalidades, perda de exclusividade, antecipação, avisos privados e intervenção administrativa foram implementados sem dependência de e-mail ou hardware.
## Evidências
- TEST-040 a TEST-047 cobertos por 10 testes de fluxo e privacidade, apoiados pelos 13 testes temporais anteriores.
- Regressão de 55 testes de backend e 3 de frontend aprovada; suítes usam bancos isolados na CI para impedir interferência de estado.
- Concorrência PostgreSQL, formatação, migrações, lint, tipos, build e estrutura aprovados na CI `32596839732` para `277c539`.

# TASK-006 — Implementar avaliações, tags e auditoria
## Estado
Concluída — GATE-006 aprovado.
## Tipo
Feature.
## Prioridade
Média.
## Origem
UC-007, UC-010; ROADMAP 0.4.0.
## Objetivo
Preservar avaliações, sugestões, fatos históricos e intervenções auditáveis.
## Escopo
### Incluído
Notas, médias derivadas, tags, auditoria, consulta e anonimização.
### Não incluído
Dashboard analítico.
## Dependências
TASK-005; GATE-005.
## Fontes de verdade obrigatórias
REQ-F-015, REQ-F-018, REQ-F-019; DECISION-006.
## Testes e portões relacionados
GATE-006; TEST-050 a TEST-053.
## Critérios de conclusão
Histórico permanece íntegro e permite consultas exemplificadas.
## Riscos
Exclusão destrutiva ou média como fonte indevida.
## Resultado
Avaliações opcionais e únicas por devolução, sugestões de tags rastreáveis, médias derivadas, auditoria imutável e consultas históricas por título, categoria e período foram implementadas. As consultas analíticas não retornam identificadores de leitores.
## Evidências
- TEST-050 a TEST-053 cobertos por 5 testes de integração, segurança e dados.
- Tentativas de editar ou excluir auditoria por instância e queryset são rejeitadas.
- Regressão de 60 testes de backend e 3 de frontend, PostgreSQL, lint, migrações e build aprovados na CI `32597411718` para `632baf1`.

# TASK-007 — Consolidar UX, acessibilidade e temas
## Estado
Em andamento — testes do GATE-007 iniciados.
## Tipo
Feature.
## Prioridade
Alta.
## Origem
UX_UI; REQ-NF-004 a REQ-NF-006 e REQ-NF-012.
## Objetivo
Completar experiência responsiva, bilíngue, acessível e os seis temas.
## Escopo
### Incluído
Estados, navegação, componentes, i18n e revisão manual AA.
### Não incluído
Mudanças de regra de negócio.
## Dependências
Fluxos funcionais; protótipos validados.
## Fontes de verdade obrigatórias
UX_UI, STYLE, REQUIREMENTS.
## Testes e portões relacionados
GATE-007; TEST-060 a TEST-064.
## Critérios de conclusão
Funções essenciais operam nos dispositivos, idiomas e temas definidos.
## Riscos
Contraste do tema translúcido e regressões mobile.

# TASK-008 — Implantar, proteger e validar a versão 1.0.0
## Estado
Planejada; depende de TASK-007.
## Tipo
Chore/Test.
## Prioridade
Alta.
## Origem
ROADMAP 1.0.0.
## Objetivo
Publicar frontend/backend, verificar segurança, carga, observabilidade e restauração.
## Escopo
### Incluído
HTTPS, CORS, backup, deploy, E2E, segurança e carga simulada.
### Não incluído
Features futuras.
## Dependências
TASK-001 a TASK-007.
## Fontes de verdade obrigatórias
Todos os documentos oficiais validados.
## Testes e portões relacionados
GATE-008; TEST-070 a TEST-074.
## Critérios de conclusão
Aceite final humano, evidências registradas e somente então tag SemVer/changelog.
## Riscos
Ambiente VPS e resultados abaixo da meta.
