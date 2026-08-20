# REQUIREMENTS.md

> Casos de uso: `UC-[ID]`; requisitos funcionais: `REQ-F-[ID]`;
> requisitos não funcionais: `REQ-NF-[ID]`; regras: `RULE-[ID]`.
> Use referências cruzadas; não codifique relações nos IDs.

## Convenções

## Representação matemática resumida opcional

Quando ela aumentar a precisão, uma interação pode ser representada por:

\[
P(\alpha,s)\land R(\alpha,s,a)
\Longrightarrow
\left[(s'=T(\alpha,s,a))\land Q(\alpha,s')\right]
\]

# Casos de uso

## UC-[ID] — [Título]
### Estado
### Ator principal
### Atores secundários
### Objetivo
### Descrição
### Pré-condições
### Gatilho
### Fluxo principal
### Fluxos alternativos
### Exceções
### Pós-condições
### Representação matemática resumida
### Requisitos funcionais envolvidos
### Regras de negócio aplicáveis
### Requisitos não funcionais relevantes
### Referências

# Requisitos funcionais

## REQ-F-[ID] — [Título]
### Estado
### Descrição
### Objetivo
### Pré-condições
### Entradas
### Saídas
### Representação matemática resumida
### Critérios de aceitação
### Casos de uso relacionados
### Regras de negócio aplicáveis
### Requisitos não funcionais relacionados
### Dependências
### Referências

---

## REQ-F-001 — Informar indisponibilidade do backend

### Estado
- [x] Aprovado

### Descrição
Quando o frontend não conseguir acessar o backend necessário para executar uma operação, ele deve informar ao usuário que o serviço está indisponível no momento.

### Objetivo
Evitar que a ausência intencional ou acidental do backend produza uma interface silenciosamente quebrada, um estado indefinido ou a impressão de que a operação foi concluída.

### Pré-condições
- O usuário acessou o frontend.
- O frontend iniciou uma operação que depende do backend.

### Entradas
- Falha de rede, erro de conexão, timeout ou resposta equivalente que torne o backend inacessível.

### Saídas
- Mensagem de erro visível e compreensível informando que não foi possível acessar o serviço.
- A operação dependente não deve ser apresentada como concluída com sucesso.

### Representação matemática resumida
Não aplicável neste momento; a forma extensiva é suficiente.

### Critérios de aceitação
- [ ] Dado que o frontend está acessível e o backend está parado ou inacessível, quando o usuário iniciar uma operação dependente do backend, então uma mensagem de indisponibilidade deve ser exibida.
- [ ] A mensagem deve explicar em linguagem compreensível que o serviço não pôde ser acessado, sem expor stack trace, segredo ou detalhe interno da infraestrutura.
- [ ] A interface não deve indicar sucesso para a operação que não pôde ser processada.
- [ ] O usuário deve poder tentar novamente por meio da própria ação ou de um controle de nova tentativa, conforme o fluxo de UX/UI que será definido.

### Casos de uso relacionados
- Pendente de definição durante a documentação inicial.

### Regras de negócio aplicáveis
- Nenhuma identificada até o momento.

### Requisitos não funcionais relacionados
- Pendente de definição durante a documentação inicial.

### Dependências
- Cliente HTTP do frontend.
- Tratamento padronizado de falhas de comunicação.
- Definição dos estados de erro em `UX_UI.md`.

### Referências
- Contexto humano informado pelo responsável em 2026-08-20.

# Requisitos não funcionais

## REQ-NF-[ID] — [Título]
### Categoria
### Estado
### Regra
### Motivo
### Escopo de aplicação
### Critério de verificação
### Prioridade
### Casos de uso relacionados
### Requisitos funcionais relacionados
### Referências

# Regras de negócio

## RULE-[ID] — [Título]
### Estado
### Regra
### Contexto
### Exceções
### Validação
### Predicado matemático
### Requisitos relacionados
### Casos de uso relacionados
### Referências
