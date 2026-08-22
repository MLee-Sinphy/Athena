# ROADMAP.md

> Versões planejadas não são entregas. Tags e `CHANGELOG.md` só serão usados após validação real.

## Visão geral
Construção incremental até a primeira versão completa `1.0.0`, com cada incremento condicionado aos portões de `TESTS.md`.

## Convenções de estado
- [x] Planejada
- [ ] Em desenvolvimento
- [ ] Em validação
- [ ] Entregue

# Versão 0.1.0 — Fundação segura
## Objetivo
Estabelecer repositório executável, banco, API, frontend e autenticação.
## Valor entregue
Primeiro acesso de leitor/administrador e comunicação segura entre camadas.
## Escopo
Bootstrap, CI, PostgreSQL, usuários, login, senha temporária, sessão em memória, i18n base e indisponibilidade da API.
## Features incluídas
Nenhuma feature futura.
## Bugs incluídos
Nenhum conhecido.
## Refatorações incluídas
Nenhuma.
## Dependências
Documentação validada e GATE-000 a GATE-002.
## Fora de escopo
Catálogo e circulação.
## Critérios de conclusão
Autenticação, autorização base, segurança e deploy de prova verificados.
## Riscos
Integração cross-origin e sessão não persistente.
## Estado
Implementada na candidata 1.0.0 — portões correspondentes aprovados; não foi publicada como entrega independente.
## Datas
- Previsão: não definida.
- Entrega real: não aplicável.

# Versão 0.2.0 — Acervo pesquisável
## Objetivo
Entregar gestão do acervo e descoberta pelo leitor.
## Valor entregue
Catálogo realista agrupado, pesquisa, tags e comparação por conservação.
## Escopo
Títulos, exemplares, mídia, estados, busca, filtros e painel administrativo do acervo.
## Features incluídas
Nenhuma feature futura.
## Bugs incluídos
Nenhum conhecido.
## Refatorações incluídas
Nenhuma.
## Dependências
0.1.0 e GATE-003.
## Fora de escopo
Reservas e empréstimos.
## Critérios de conclusão
UC-002 e parte administrativa de UC-008 verificadas.
## Riscos
Licenças de capas e desempenho de busca.
## Estado
Implementada na candidata 1.0.0 — portão correspondente aprovado; não foi publicada como entrega independente.
## Datas
- Previsão: não definida.
- Entrega real: não aplicável.

# Versão 0.3.0 — Circulação
## Objetivo
Entregar reservas, fila, retirada, empréstimo e devolução.
## Valor entregue
Fluxo principal físico-digital completo.
## Escopo
Calendário, disponibilidade, concorrência, fila, alterações, cancelamentos, renovação e avisos internos.
## Features incluídas
Componente interno de disponibilidade antecipada; e-mail permanece em FEATURE-001.
## Bugs incluídos
Nenhum conhecido.
## Refatorações incluídas
Nenhuma.
## Dependências
0.2.0 e GATE-004/GATE-005.
## Fora de escopo
E-mail e hardware.
## Critérios de conclusão
UC-003 a UC-006 verificados sem sobreposição concorrente.
## Riscos
Complexidade temporal e concorrência.
## Estado
Implementada na candidata 1.0.0 — portões correspondentes aprovados; não foi publicada como entrega independente.
## Datas
- Previsão: não definida.
- Entrega real: não aplicável.

# Versão 0.4.0 — Governança e histórico
## Objetivo
Completar políticas, penalidades, avaliações e auditoria.
## Valor entregue
Instituição configurável e dados preparados para análises.
## Escopo
Painel de políticas, vigência, penalidades, avaliações, tags sugeridas, auditoria e anonimização.
## Features incluídas
Nenhuma feature futura.
## Bugs incluídos
Nenhum conhecido.
## Refatorações incluídas
Nenhuma.
## Dependências
0.3.0 e GATE-006.
## Fora de escopo
Dashboards analíticos; apenas dados suficientes.
## Critérios de conclusão
UC-007 a UC-010 verificados.
## Riscos
Retenção e interpretação de políticas alteradas.
## Estado
Implementada na candidata 1.0.0 — portão correspondente aprovado; não foi publicada como entrega independente.
## Datas
- Previsão: não definida.
- Entrega real: não aplicável.

# Versão 1.0.0 — Primeira versão validada
## Objetivo
Consolidar o produto de estudo completo e demonstrável.
## Valor entregue
Sistema bilíngue, responsivo, acessível, seguro, implantável e testado.
## Escopo
Todo o escopo inicial de `PROJECT.md`, seis temas, backup restaurável, observabilidade e carga simulada.
## Features incluídas
Somente capacidades da primeira versão formalizadas em requisitos.
## Bugs incluídos
Bugs bloqueadores encontrados na validação.
## Refatorações incluídas
Somente as necessárias para critérios de aceite.
## Dependências
0.4.0 e GATE-007/GATE-008.
## Fora de escopo
E-mail, hardware, múltiplas instituições, pagamentos e livros digitais.
## Critérios de conclusão
Todos os critérios finais de `TESTS.md`, documentação e validação humana aprovados.
## Riscos
Amplitude dos testes de acessibilidade, segurança e carga.
## Estado
Em validação — candidata implementada na cadeia de branches; ainda não entregue nem versionada.
## Datas
- Previsão: não definida.
- Entrega real: não aplicável.

## Horizontes futuros sem versão aprovada
- FEATURE-001: e-mails de disponibilidade antecipada.
- FEATURE-002: recuperação autônoma de senha por e-mail.
- FEATURE-003: retirada e devolução por leitor físico.
- Dashboards analíticos baseados no histórico preservado.
