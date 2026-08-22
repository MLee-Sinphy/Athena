# TESTS.md

> Estratégia e portões aprovados em 2026-08-22. Cada incremento exige a falha inicial correta e a regressão acumulada definida aqui.

## Objetivo
Guiar incrementos por falha inicial comprovada, regressão acumulada e evidência proporcional ao risco.

## Princípios
- Cada incremento começa pelo teste do próximo portão.
- O teste novo falha pelo motivo correto antes da implementação.
- Avanço exige teste atual e regressão acumulada aprovados.
- Testes não inventam regras de negócio.
- PostgreSQL real é obrigatório para concorrência e constraints específicas.

## Convenções
- Casos: `TEST-[ID]`; portões: `GATE-[ID]`; suítes: `SUITE-[ID]`.
- Estado inicial dos casos: Planejado; a execução depende da tarefa e do portão correspondentes.

## Estratégia por ordem crescente de implementação
### Nível 0 — Infraestrutura e verificações estáticas
Formatação, lint, tipos, build, migrações e detecção de segredos.
### Nível 1 — Fundamentos e unidades independentes
Senha, calendário, políticas, penalidades e transições puras.
### Nível 2 — Componentes e módulos
Componentes React, serializers, serviços e autorização isolada.
### Nível 3 — Integração interna
API, ORM, PostgreSQL, storage, auditoria e concorrência.
### Nível 4 — Contratos e integrações externas controladas
OpenAPI, cliente React, CORS, HTTPS e backup.
### Nível 5 — Fluxos e subsistemas
Casos de uso completos por perfil.
### Nível 6 — Ponta a ponta e sistema completo
GitHub Pages para VPS e falhas reais controladas.
### Nível 7 — Qualidades transversais e aceitação final
Acessibilidade, segurança, compatibilidade, carga e restauração.

## Ambientes
### Local
Containers ou serviços reproduzíveis; PostgreSQL dedicado a testes.
### Integração
Ambiente efêmero com build equivalente ao deploy.
### Homologação
GitHub Pages e VPS de demonstração sem dados pessoais reais.

## Dados, fixtures e isolamento
Pessoas sintéticas; livros reais somente com uso legal; relógio controlável; factories determinísticas; transações isoladas; nenhum teste depende da ordem de execução.

## Suítes
### SUITE-001 — Verificações rápidas
#### Objetivo
Feedback por commit.
#### Níveis incluídos
0 a 2.
#### Casos incluídos
TEST-001, 002, 010, 020, 030 e unidades derivadas.
#### Comando
Definido no bootstrap e documentado no README.
#### Quando executar
Antes de commit e em todo push.
#### Critério de aprovação
Zero falha, warning novo ou segredo detectado.

### SUITE-002 — Integração e regressão
#### Objetivo
Validar contratos e domínio persistido.
#### Níveis incluídos
0 a 5.
#### Casos incluídos
Todos exceto carga completa e revisão manual.
#### Quando executar
Antes de avançar portão e em CI principal.
#### Critério de aprovação
Todos os casos automatizados aprovados no PostgreSQL alvo.

### SUITE-003 — Aceitação 1.0
#### Objetivo
Validar sistema publicado e qualidades transversais.
#### Níveis incluídos
0 a 7.
#### Casos incluídos
Todos os TESTs e checklists manuais.
#### Quando executar
Candidata à versão 1.0.0.
#### Critério de aprovação
Zero bloqueador; desvios não bloqueadores documentados e aceitos.

## Sequência de portões
| Portão | Incremento | Condição para avançar | Tarefa |
|---|---|---|---|
| GATE-000 | documentação e bootstrap | **Aprovado** — validação humana, build/lint/testes base | TASK-001 |
| GATE-001 | modelo de contas | **Aprovado** — unidades de senha/perfis falharam e depois passaram | TASK-002 |
| GATE-002 | autenticação ponta a ponta | **Aprovado** — autorização, sessão e indisponibilidade passam | TASK-002 |
| GATE-003 | acervo e catálogo | **Aprovado** — CRUD, agrupamento, busca e privacidade passam | TASK-003 |
| GATE-004 | calendário e disponibilidade | **Aprovado** — bordas e concorrência PostgreSQL passam | TASK-004 |
| GATE-005 | circulação | **Aprovado** — reserva até devolução, fila e avisos passam | TASK-005 |
| GATE-006 | governança histórica | **Aprovado** — penalidades, auditoria, avaliações e análises passam | TASK-006 |
| GATE-007 | experiência completa | **Aprovado** — responsividade, i18n, temas e AA aplicável passam | TASK-007 |
| GATE-008 | aceite 1.0 | deploy, segurança, backup, E2E e carga passam | TASK-008 |

GATE-000 a GATE-007 foram aprovados em 2026-08-22. O GATE-008 permanece **Planejado**. A regressão exigida em cada linha inclui todos os portões anteriores.

## Casos de teste
| ID | Nível | Tipo | Objetivo e resultado esperado | Fonte |
|---|---:|---|---|---|
| TEST-001 | 0 | estático | **Aprovado:** formatação, lint, tipos e build sem erro | STYLE |
| TEST-002 | 0 | segurança | **Aprovado:** scanner não encontra segredo ou credencial real | CON-005 |
| TEST-003 | 3 | banco | **Aprovado:** migrações e teste da API executam em PostgreSQL vazio | ARCHITECTURE |
| TEST-010 | 1 | unidade | **Aprovado:** política de senha, perfis e identidades aceitam/rejeitam limites definidos | REQ-NF-002 |
| TEST-011 | 3 | integração | **Aprovado:** e-mail e matrícula autenticam sem enumeração | REQ-F-001 |
| TEST-012 | 5 | fluxo | **Aprovado:** senha temporária obriga troca e recuperação assistida revoga sessão | REQ-F-002 |
| TEST-013 | 3 | segurança | **Aprovado:** matriz de perfil/propriedade bloqueia acesso indevido | REQ-NF-001 |
| TEST-014 | 6 | E2E | **Aprovado:** API desligada produz mensagem e nenhum falso sucesso | REQ-F-020 |
| TEST-020 | 3 | integração | **Aprovado:** catálogo agrupa título e preserva exemplares | RULE-003 |
| TEST-021 | 3 | integração | **Aprovado:** busca encontra descrição e tags; ISBN ausente é válido | REQ-F-005 |
| TEST-022 | 5 | fluxo | **Aprovado:** leitor escolhe exemplar pela conservação sem ver código | REQ-F-005 |
| TEST-023 | 3 | segurança | **Aprovado:** upload inválido é rejeitado e mídia autorizada funciona | ARCHITECTURE |
| TEST-030 | 1 | unidade | **Aprovado:** calendário cobre fechamentos, mínimo/máximo e bordas | RULE-005 |
| TEST-031 | 1 | unidade | **Aprovado:** penalidades cobrem atraso e janela de cancelamento | RULE-012 |
| TEST-032 | 3 | concorrência | **Aprovado:** duas reservas simultâneas não usam o mesmo exemplar/período | RULE-007 |
| TEST-033 | 3 | integração | **Aprovado:** FIFO e desempate são determinísticos e privados | RULE-008 |
| TEST-034 | 3 | integração | **Aprovado:** mudança de política preserva reservas existentes | RULE-015 |
| TEST-040 | 5 | fluxo | **Aprovado:** reserva válida é automática e recusa explica regra | REQ-F-006 |
| TEST-041 | 5 | fluxo | **Aprovado:** retirada cria empréstimo somente na confirmação física | RULE-009 |
| TEST-042 | 5 | fluxo | **Aprovado:** devolução encerra uma vez e libera disponibilidade | REQ-F-010 |
| TEST-043 | 5 | fluxo | **Aprovado:** ausente retira enquanto livre e perde intervalo após conflito | RULE-010 |
| TEST-044 | 5 | fluxo | **Aprovado:** próximo aceita/recusa antecipação sem perder data final | RULE-010 |
| TEST-045 | 5 | fluxo | **Aprovado:** alteração/cancelamento respeitam conflito e contagem | RULE-011/012 |
| TEST-046 | 5 | fluxo | **Aprovado:** renovação exige ausência de fila e máximo | REQ-F-013 |
| TEST-047 | 3 | privacidade | **Aprovado:** avisos e fila não expõem outras pessoas | REQ-NF-009 |
| TEST-050 | 3 | integração | **Aprovado:** notas 1–5 são opcionais, únicas por devolução e não editáveis | RULE-013 |
| TEST-051 | 3 | integração | **Aprovado:** tags preservam autor/data e participam da busca | RULE-013 |
| TEST-052 | 3 | segurança | **Aprovado:** auditoria é completa e imutável por operação comum | REQ-F-019 |
| TEST-053 | 3 | dados | **Aprovado:** histórico responde aos exemplos analíticos após anonimização | DECISION-006 |
| TEST-060 | 2 | componente | **Aprovado:** estados de UI e formulários são acessíveis | UX_UI |
| TEST-061 | 6 | E2E | **Aprovado:** jornadas essenciais funcionam a partir de 320 px e desktop | REQ-NF-004 |
| TEST-062 | 2 | i18n | **Aprovado:** pt-BR/en completos, seleção inicial e troca persistente | REQ-NF-006 |
| TEST-063 | 7 | acessibilidade | **Aprovado no escopo do GATE-007:** automação e revisão registrada atendem WCAG 2.2 AA aplicável | REQ-NF-005 |
| TEST-064 | 2 | visual | **Aprovado:** seis temas usam tokens, contraste válido e fallback opaco | REQ-NF-012 |
| TEST-070 | 6 | E2E | GitHub Pages consome VPS por HTTPS/CORS corretos | CON-002 |
| TEST-071 | 7 | segurança | sessão, token, rate limit, autorização e uploads resistem à suíte | REQ-NF-001/003 |
| TEST-072 | 7 | operação | backup conjunto restaura banco e mídia com checksums | REQ-NF-010 |
| TEST-073 | 7 | carga | volumes e 500 simultâneos são simulados e documentados | REQ-NF-008 |
| TEST-074 | 7 | compatibilidade | navegadores alvo e tecnologias assistivas passam checklist | REQ-NF-004/005 |

## Matriz de rastreabilidade
| Fonte | Critério ou comportamento | Testes | Portões | Estado |
|---|---|---|---|---|
| UC-001 | acesso e credenciais | 010–014 | 001–002 | Planejado |
| UC-002/008 | catálogo e acervo | 020–023 | 003 | Planejado |
| UC-003/009 | calendário e reserva | 030–040 | 004–005 | Planejado |
| UC-004/005/006 | circulação e avisos | 041–047 | 005 | Planejado |
| UC-007/010 | avaliações, histórico e auditoria | 050–053 | 006 | Planejado |
| REQ-NF-004/005/006/012 | experiência | 060–064 | 007 | Planejado |
| REQ-NF-001/003/008/010 | aceite operacional | 070–074 | 008 | Planejado |

## Regressão acumulada
| Após o portão | Testes e suítes obrigatórios | Resultado exigido |
|---|---|---|
| 000–003 | SUITE-001 + testes do portão | GATE-000 aprovado; próximos exigem 100% |
| 004–007 | SUITE-001 e SUITE-002 | 100% aprovados |
| 008 | SUITE-003 | aceite final registrado |

## Critérios finais da versão
- Todos os requisitos obrigatórios possuem teste ou evidência manual aprovada.
- Nenhuma falha crítica/alta aberta, segredo versionado ou dado pessoal real.
- Backup restaurado, carga registrada e deploy publicado verificado.
- Responsável valida o comportamento e autoriza a entrega antes da tag `1.0.0`.
