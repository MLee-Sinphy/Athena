# DECISIONS.md

> Registro das decisões arquiteturais e de produto com impacto amplo.

# DECISION-001 — SPA React no GitHub Pages
## Estado
Aprovada.
## Data
2026-08-22.
## Responsável
Lee.
## Contexto
Frontend público separado do backend sob demanda.
## Problema
Publicar uma SPA sem servidor de fallback.
## Decisão
React com TypeScript e `HashRouter` no endereço padrão do GitHub Pages.
## Motivação
Objetivo de estudo, hospedagem simples e rotas compatíveis.
## Alternativas consideradas
BrowserRouter com fallback, SSR, servidor único.
## Consequências
### Positivas
Deploy estático e independente.
### Negativas
URLs contêm fragmento e API possui outra origem.
### Riscos
CORS ou configuração HTTPS incorretos.
## Documentos afetados
`ARCHITECTURE.md`, `UX_UI.md`, `CONSTRAINTS.md`.
## Critério para revisar esta decisão
Domínio próprio ou hospedagem com fallback de SPA.
## Substitui
Nenhuma.
## Substituída por
Nenhuma.

# DECISION-002 — Django/DRF com PostgreSQL
## Estado
Aprovada.
## Data
2026-08-22.
## Responsável
Lee.
## Contexto
Domínio relacional com autenticação, concorrência e auditoria.
## Problema
Escolher backend e banco adequados ao estudo e às regras.
## Decisão
Python, Django, DRF, Django ORM e PostgreSQL em VPS Hostinger.
## Motivação
Familiaridade com Python e recursos maduros de segurança, administração, migração e transações.
## Alternativas consideradas
FastAPI, Node.js, SQLite e MySQL.
## Consequências
### Positivas
Ecossistema integrado e banco robusto.
### Negativas
Exige operação de VPS.
### Riscos
Configuração e manutenção do servidor.
## Documentos afetados
`ARCHITECTURE.md`, `CONSTRAINTS.md`.
## Critério para revisar esta decisão
Incompatibilidade comprovada com o ambiente ou objetivos.
## Substitui
Nenhuma.
## Substituída por
Nenhuma.

# DECISION-003 — Token opaco somente em memória
## Estado
Aprovada.
## Data
2026-08-22.
## Responsável
Lee.
## Contexto
Frontend e backend estão em origens diferentes.
## Problema
Autenticar sem persistir credencial reutilizável no navegador.
## Decisão
Token bearer opaco, revogável e curto, com digest no backend e valor somente na memória do React.
## Motivação
Reduzir exposição por storage web e manter revogação.
## Alternativas consideradas
JWT persistente e cookie de sessão cross-site.
## Consequências
### Positivas
Sem token durável no navegador.
### Negativas
Reload pode exigir login; tabela e limpeza de tokens.
### Riscos
XSS ainda pode acessar token em memória durante a sessão.
## Documentos afetados
`ARCHITECTURE.md`, `REQUIREMENTS.md`, `CONSTRAINTS.md`.
## Critério para revisar esta decisão
Necessidade validada de sessão persistente ou domínio compartilhado.
## Substitui
Nenhuma.
## Substituída por
Nenhuma.

# DECISION-004 — Separar título e exemplar
## Estado
Aprovada.
## Data
2026-08-22.
## Responsável
Lee.
## Contexto
O catálogo deve ser simples, mas cada cópia física rastreável.
## Problema
Representar cópias equivalentes e conservação distinta.
## Decisão
Título agrega metadados; exemplar possui código, estado e avaliação física. Leitor escolhe exemplar apenas quando desejar comparar conservação.
## Motivação
Equilibrar simplicidade e controle físico.
## Alternativas consideradas
Uma linha por cópia no catálogo ou alocação sempre automática.
## Consequências
### Positivas
Catálogo limpo e escolha informada.
### Negativas
Disponibilidade precisa considerar título e cópia.
### Riscos
Condições de corrida na escolha.
## Documentos afetados
`REQUIREMENTS.md`, `ARCHITECTURE.md`, `UX_UI.md`.
## Critério para revisar esta decisão
Acervo sem necessidade de rastrear cópias.
## Substitui
Nenhuma.
## Substituída por
Nenhuma.

# DECISION-005 — Reserva vira empréstimo na retirada
## Estado
Aprovada.
## Data
2026-08-22.
## Responsável
Lee.
## Contexto
Reserva garante um período, mas o livro continua fisicamente na biblioteca.
## Problema
Definir o início inequívoco do empréstimo.
## Decisão
Somente confirmação da retirada física cria empréstimo ativo.
## Motivação
Representar corretamente posse e atrasos de retirada.
## Alternativas consideradas
Concessão ou data prevista como início automático.
## Consequências
### Positivas
Estado reflete a realidade física.
### Negativas
Exige confirmação administrativa na v1.
### Riscos
Equipe esquecer de registrar a retirada.
## Documentos afetados
`REQUIREMENTS.md`, `ARCHITECTURE.md`.
## Critério para revisar esta decisão
Integração física automatizada futura.
## Substitui
Nenhuma.
## Substituída por
Nenhuma.

# DECISION-006 — Preservar fatos e derivar estatísticas
## Estado
Aprovada.
## Data
2026-08-22.
## Responsável
Lee.
## Contexto
Análises futuras ainda não estão definidas.
## Problema
Permitir inferências sem antecipar tabelas analíticas frágeis.
## Decisão
Preservar eventos datados e relações de circulação, avaliações, estados e tags; calcular agregados por consultas ou projeções reconstruíveis.
## Motivação
Flexibilidade analítica e fonte de verdade simples.
## Alternativas consideradas
Contadores mutáveis nos registros principais e tabelas estatísticas prematuras.
## Consequências
### Positivas
Novas análises podem usar o histórico original.
### Negativas
Consultas futuras podem exigir índices ou projeções.
### Riscos
Retenção inadequada comprometer análises.
## Documentos afetados
`ARCHITECTURE.md`, `REQUIREMENTS.md`, `CONSTRAINTS.md`.
## Critério para revisar esta decisão
Volume medido justificar data warehouse ou projeções persistentes.
## Substitui
Nenhuma.
## Substituída por
Nenhuma.

# DECISION-007 — Open Library para enriquecimento e capas externas
## Estado
Aprovada.
## Data
2026-08-22.
## Responsável
Lee.
## Contexto
O catálogo demonstrativo precisa de dados realistas sem aumentar desnecessariamente o banco e o volume de mídia.
## Problema
Obter metadados e capas mantendo o backend sob demanda e leve.
## Decisão
Usar a API pública da Open Library em importações identificadas e de baixo volume. Persistir somente metadados essenciais e URL da fonte; o frontend carrega capas diretamente pelo ISBN, com fallback local.
## Motivação
Serviço gratuito e alinhado a bibliotecas/educação, menor uso de armazenamento e seed realista.
## Alternativas consideradas
Google Books com chave, upload de todas as capas e armazenamento binário no PostgreSQL.
## Consequências
### Positivas
Menor backup e tráfego do backend; dados demonstrativos mais realistas.
### Negativas
Capas dependem de um serviço externo e podem variar ou faltar.
### Riscos
Rate limit, indisponibilidade e metadados de edições divergentes; curadoria local e fallback permanecem obrigatórios.
## Documentos afetados
`ARCHITECTURE.md`, `REQUIREMENTS.md`, `UX_UI.md`, `OPERATIONS.md`.
## Critério para revisar esta decisão
Uso comercial, alto volume, exigência de controle integral das imagens ou mudança das diretrizes da Open Library.
## Substitui
Nenhuma.
## Substituída por
Nenhuma.
