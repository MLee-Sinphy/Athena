# CONSTRAINTS.md

> Restrições oficiais. Todas estão aprovadas no contexto humano, mas a documentação completa ainda aguarda validação final.

## CON-001 — Implantação isolada por instituição
### Categoria
Produto e dados.
### Estado
Aprovada.
### Restrição
Cada implantação atende somente uma instituição.
### Motivo
Reduzir complexidade e manter acervo, usuários e políticas isolados.
### Consequências
Não haverá tenancy compartilhada na primeira versão.
### Verificação
Revisão de modelo, configuração e testes de autorização.
### Exceções permitidas
Nenhuma na primeira versão.
### Documentos relacionados
`PROJECT.md`, `ARCHITECTURE.md`, `REQUIREMENTS.md`.

## CON-002 — Tecnologias e hospedagem
### Categoria
Técnica.
### Estado
Aprovada.
### Restrição
React com `HashRouter` no GitHub Pages; API Python com Django/DRF, PostgreSQL e Django ORM em VPS Hostinger; comunicação por HTTPS.
### Motivo
Objetivos de estudo, familiaridade do responsável e ambientes escolhidos.
### Consequências
Frontend e API possuem origens distintas; CORS deve ser restrito.
### Verificação
Build, deploy e teste de integração publicado.
### Exceções permitidas
Ambiente local equivalente para desenvolvimento e testes.
### Documentos relacionados
`ARCHITECTURE.md`, `DECISIONS.md`.

## CON-003 — Backend sob demanda
### Categoria
Operação.
### Estado
Aprovada.
### Restrição
Não há disponibilidade 24 horas; funções dinâmicas dependem do backend ativo.
### Motivo
Projeto de estudo.
### Consequências
O frontend deve comunicar indisponibilidade e jamais indicar sucesso indevido.
### Verificação
Teste ponta a ponta com API desligada.
### Exceções permitidas
Nenhuma para a comunicação de erro.
### Documentos relacionados
`REQUIREMENTS.md`, `UX_UI.md`.

## CON-004 — Recursos gratuitos por padrão
### Categoria
Financeira.
### Estado
Aprovada.
### Restrição
Priorizar recursos gratuitos; qualquer serviço pago exige aprovação explícita.
### Motivo
Natureza educacional do projeto.
### Consequências
E-mail e armazenamento externo não podem ser assumidos silenciosamente.
### Verificação
Revisão de dependências e custos antes da adoção.
### Exceções permitidas
Serviço aprovado pelo responsável.
### Documentos relacionados
`ARCHITECTURE.md`, `FEATURES.md`.

## CON-005 — Privacidade e dados de demonstração
### Categoria
Legal e segurança.
### Estado
Aprovada.
### Restrição
Dados pessoais de demonstração são sintéticos; filas não revelam outras pessoas; metadados e imagens reais exigem uso legal.
### Motivo
Privacidade e direitos autorais.
### Consequências
Fixtures não podem reproduzir pessoas reais e capas precisam de licença adequada.
### Verificação
Revisão de fixtures, permissões e conteúdo versionado.
### Exceções permitidas
Metadados bibliográficos legalmente utilizáveis.
### Documentos relacionados
`REQUIREMENTS.md`, `TESTS.md`.

## CON-006 — Credencial não persistente no navegador
### Categoria
Segurança.
### Estado
Aprovada.
### Restrição
Token bearer opaco permanece somente na memória do frontend.
### Motivo
Reduzir exposição a scripts e evitar credenciais reutilizáveis em storage web.
### Consequências
Recarregar ou reabrir a aplicação pode exigir login.
### Verificação
Inspeção do código e testes de segurança.
### Exceções permitidas
Nenhuma sem nova decisão arquitetural.
### Documentos relacionados
`ARCHITECTURE.md`, `DECISIONS.md`.

## CON-007 — Acessibilidade e responsividade
### Categoria
Qualidade.
### Estado
Aprovada.
### Restrição
Todas as funções essenciais devem operar em computador e smartphone, com meta WCAG 2.2 AA.
### Motivo
Acesso inclusivo e requisito fundamental do produto.
### Consequências
Componentes, temas e fluxos exigem verificação automatizada e manual.
### Verificação
Testes de viewport, teclado, leitor de tela e critérios aplicáveis AA.
### Exceções permitidas
Nenhuma função essencial exclusiva de um dispositivo.
### Documentos relacionados
`UX_UI.md`, `TESTS.md`.

## CON-008 — Preservação histórica
### Categoria
Dados.
### Estado
Aprovada.
### Restrição
Empréstimos, avaliações e auditoria não podem ser eliminados por operações comuns; anonimização deve preservar relações analíticas.
### Motivo
Rastreabilidade e análises futuras.
### Consequências
Exclusões são administrativas e preferem anonimização; estatísticas derivam de eventos históricos.
### Verificação
Testes de integridade e retenção.
### Exceções permitidas
Política legal posterior formalmente documentada.
### Documentos relacionados
`ARCHITECTURE.md`, `REQUIREMENTS.md`.
