# FEATURES.md

> Capacidades da primeira versão pertencem aos requisitos; use este arquivo para possibilidades futuras.

# FEATURE-[ID] — [Título]
## Estado
## Origem
## Problema ou oportunidade
## Público beneficiado
## Proposta
## Benefício esperado
## Alinhamento com o projeto
## Fluxo esperado
## Escopo inicial
## Fora de escopo
## Critérios iniciais de sucesso
## Dependências
## Riscos
## Impactos possíveis
## Documentos que precisam ser atualizados
## Referências
## Resultado

---

# FEATURE-001 — Notificações de disponibilidade antecipada

## Estado
- [x] Adiada

## Origem
- Usuário: contexto fornecido pelo responsável em 2026-08-20.

## Problema ou oportunidade
Uma devolução antecipada ou a expiração de uma reserva sem retirada pode liberar um exemplar antes da data reservada pelo próximo leitor da fila, mas esse leitor pode não perceber a nova disponibilidade.

## Público beneficiado
Leitores que aguardam um exemplar já reservado para um período futuro.

## Proposta
Notificar o próximo leitor elegível dentro do sistema e por e-mail quando uma devolução antecipada ou a perda de prioridade de outra reserva permitir a retirada antes da data inicialmente reservada.

## Benefício esperado
Antecipar o acesso ao livro e melhorar o aproveitamento do acervo sem retirar do leitor a data final já organizada.

## Alinhamento com o projeto
A capacidade complementa a fila de espera e a política de antecipação por devolução, mas não é necessária para validar a primeira versão do fluxo principal.

## Fluxo esperado
1. Um exemplar é devolvido antes da data prevista.
2. O sistema identifica o próximo leitor elegível na fila.
3. O sistema cria uma notificação interna e envia um e-mail informando a disponibilidade antecipada.
4. O sistema registra o envio e, quando ocorrerem, a leitura, o aceite ou a recusa.
5. O leitor pode aceitar ou recusar a antecipação até a data original de início de sua reserva.
6. Se aceitar, pode retirar o exemplar antes da data reservada conforme as regras vigentes.
7. Se recusar, preserva integralmente sua reserva original.
8. A data final originalmente reservada é preservada, mesmo que isso gere a exceção aprovada ao período máximo normal.

## Escopo inicial
- Notificação interna e por e-mail para disponibilidade antecipada causada por devolução antes do prazo ou reserva não retirada.
- Identificação do próximo leitor elegível.
- Registro de envio, leitura, aceite e recusa.

## Fora de escopo
- Implementação na primeira versão.
- Definição antecipada do provedor de e-mail.
- Notificações não relacionadas à disponibilidade antecipada.

## Critérios iniciais de sucesso
- As notificações são destinadas somente ao próximo leitor elegível.
- A mensagem informa de forma compreensível que a retirada pode ser antecipada.
- Nenhuma notificação altera silenciosamente as datas confirmadas.
- O leitor pode responder até a data original de início de sua reserva.
- Uma recusa não cancela nem modifica a reserva original.

## Dependências
- Fila de espera implementada e validada.
- Registro de devolução antecipada.
- Endereço de e-mail válido do leitor.
- Central interna de notificações ainda não implementada.
- Serviço de envio de e-mails ainda não escolhido.

## Riscos
- Envio duplicado, atrasado ou para pessoa inelegível.
- Dependência e possível custo de serviço externo.
- Tratamento de dados pessoais e consentimento aplicável.

## Impactos possíveis
- Produto: acrescenta comunicação proativa.
- UX/UI: exige preferências e estados de notificação.
- Arquitetura: exige integração assíncrona ou mecanismo confiável de envio.
- Dados: exige registrar tentativa e resultado do envio.
- Segurança: exige proteger endereço e conteúdo do e-mail.
- Desempenho: não deve bloquear a devolução.
- Documentação: requisitos, arquitetura, UX/UI, testes e decisões deverão ser atualizados quando a feature for priorizada.

## Documentos que precisam ser atualizados
- Pendente até aprovação e priorização futura.

## Referências
- Review: Não aplicável; origem anterior à primeira versão.
- Roadmap: Não incluída.
- Requisito: Pendente.
- Decisão: Pendente.
- Tarefa: Pendente.

## Resultado
- Versão entregue: Não entregue.
- Data: Não aplicável.
