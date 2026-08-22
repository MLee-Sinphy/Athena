# STYLE.md

> Padrões técnicos propostos para frontend, backend, testes e documentação.

## Princípios gerais
Clareza, tipos explícitos, funções pequenas, dependências direcionadas ao domínio e ausência de abstração sem uso real.
## Organização do código
Separar interface, aplicação, domínio e persistência. Features frontend agrupam UI, hooks e contratos próprios; apps Django seguem limites de domínio.
## Estrutura de pastas
Usar a estrutura proposta em `ARCHITECTURE.md`; testes próximos ao código quando unitários e diretórios próprios para integração/E2E.
## Nomenclatura
### Arquivos
Frontend conforme convenção do ecossistema; Python em `snake_case`; Markdown oficial em maiúsculas conforme estrutura atual.
### Pastas
Minúsculas, sem espaços, orientadas a responsabilidade.
### Variáveis
Nomes descritivos; `camelCase` em TypeScript e `snake_case` em Python.
### Funções
Verbos que expressem efeito ou consulta.
### Classes
`PascalCase`; nomes de domínio, não padrões genéricos.
### Componentes
`PascalCase`, uma responsabilidade visual principal.
### Constantes
`UPPER_SNAKE_CASE`; valores configuráveis não são constantes escondidas.
## Funções
Evitar booleanos ambíguos, efeitos implícitos e parâmetros excessivos; retornos e erros devem ser previsíveis.
## Componentes
Sem regra de negócio no componente; acessibilidade faz parte da API; cores apenas por tokens.
## Comentários
### Quando comentar
Motivação, invariantes, decisão incomum e limitação externa.
### Quando não comentar
Não repetir código nem preservar código morto comentado.
## Documentação interna
Docstrings em APIs públicas ou lógica não evidente; contratos REST documentados por OpenAPI.
## Tratamento de erros
Erros de domínio tipados e traduzidos na borda; nunca capturar silenciosamente; interface não mostra stack trace.
## Logs
Estruturados e correlacionáveis; não registrar segredos ou dados pessoais desnecessários.
## Testes
### Organização
Pirâmide de testes com integração real para comportamento dependente do PostgreSQL.
### Nomenclatura
Descrever condição, ação e resultado; IDs oficiais em comentários/metadados quando houver rastreabilidade.
### Casos obrigatórios
Sucesso, fronteiras, autorização, concorrência, falha, acessibilidade e regressão relevante.
## Dependências
Fixar versões, justificar novas bibliotecas, verificar manutenção/licença e remover as não usadas.
## Segurança
Validação no backend, menor privilégio, saída segura, secrets fora do Git e revisão de upload/consultas.
## Acessibilidade
HTML semântico primeiro; ARIA apenas quando necessário; testes automatizados não substituem revisão manual.
## Desempenho
Medir antes de otimizar; evitar N+1, renderizações desnecessárias e payloads ilimitados.
## Padrões proibidos
Regras em views/componentes, token em storage web, `except` vazio, SQL concatenado, cores literais fora dos temas, dependência paga não aprovada e exclusão destrutiva de histórico.
## Formatação automática
Ferramentas oficiais escolhidas no bootstrap devem rodar em CI sem divergência local.
## Lint
Lint estrito para TypeScript/React e Python; warnings novos falham na CI.
## Observações específicas da linguagem
Python usa type hints no código de aplicação; TypeScript usa modo estrito e evita `any` sem justificativa.
