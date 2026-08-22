# TASKS.md

> Plano executável proposto. Todas as tarefas estão bloqueadas até a validação humana integral da documentação oficial.

# TASK-001 — Inicializar frontend, backend e qualidade
## Estado
Bloqueada por validação documental.
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

# TASK-002 — Implementar contas e autenticação
## Estado
Bloqueada por TASK-001 e validação.
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

# TASK-003 — Implementar acervo e catálogo
## Estado
Bloqueada por TASK-002 e validação.
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

# TASK-004 — Implementar calendário, políticas e disponibilidade
## Estado
Bloqueada por TASK-003 e validação.
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

# TASK-005 — Implementar circulação, fila e avisos
## Estado
Bloqueada por TASK-004 e validação.
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

# TASK-006 — Implementar avaliações, tags e auditoria
## Estado
Bloqueada por TASK-005 e validação.
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

# TASK-007 — Consolidar UX, acessibilidade e temas
## Estado
Bloqueada por TASK-006 e validação.
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
Bloqueada por TASK-007 e validação.
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
