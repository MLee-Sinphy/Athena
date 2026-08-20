# TESTS.md

> Planeje casos e portões antecipadamente, mas construa testes executáveis de modo incremental.

## Objetivo

## Princípios
- Cada incremento começa pelo teste do próximo portão.
- O teste novo deve falhar pelo motivo correto.
- O próximo portão exige o teste atual e a regressão acumulada aprovados.
- A derivação de testes não pode inventar regras de negócio.

## Convenções
- Casos: `TEST-[ID]`.
- Portões: `GATE-[ID]`.
- Suítes: `SUITE-[ID]`.

## Estratégia por ordem crescente de implementação
### Nível 0 — Infraestrutura e verificações estáticas
### Nível 1 — Fundamentos e unidades independentes
### Nível 2 — Componentes e módulos
### Nível 3 — Integração interna
### Nível 4 — Contratos e integrações externas controladas
### Nível 5 — Fluxos e subsistemas
### Nível 6 — Ponta a ponta e sistema completo
### Nível 7 — Qualidades transversais e aceitação final

## Ambientes
### Local
### Integração
### Homologação

## Dados, fixtures e isolamento

## Suítes
### SUITE-[ID] — [Título]
#### Objetivo
#### Níveis incluídos
#### Casos incluídos
#### Comando
#### Quando executar
#### Critério de aprovação

## Sequência de portões
### GATE-[ID] — [Título]
#### Ordem
#### Estado
#### Objetivo do incremento
#### Testes deste portão
#### Regressão acumulada obrigatória
#### Dependências
#### Condição para iniciar
#### Condição para avançar
#### Tarefas relacionadas
#### Resultado

## Casos de teste
### TEST-[ID] — [Título]
#### Estado
#### Ordem de implementação
#### Nível
#### Tipo
#### Objetivo
#### Fontes de verdade verificadas
#### Tarefas relacionadas
#### Pré-condições
#### Dados de teste
#### Procedimento
#### Resultado esperado
#### Casos e variações cobertos
#### Automação
#### Confirmação da falha inicial
#### Resultado após a implementação
#### Riscos de falso positivo ou falso negativo
#### Referências

## Matriz de rastreabilidade
| Fonte | Critério ou comportamento | Testes | Portões | Estado |
|---|---|---|---|---|

## Regressão acumulada
| Após o portão | Testes e suítes obrigatórios | Comando | Resultado exigido |
|---|---|---|---|

## Critérios finais da versão
