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

# FEATURE-001 — Notificação de disponibilidade antecipada por e-mail

## Estado
- [x] Adiada

## Origem
- Usuário: contexto fornecido pelo responsável em 2026-08-20.

## Problema ou oportunidade
Uma devolução antecipada pode liberar um exemplar antes da data reservada pelo próximo leitor da fila, mas esse leitor pode não perceber a nova disponibilidade.

## Público beneficiado
Leitores que aguardam um exemplar já reservado para um período futuro.

## Proposta
Enviar um e-mail ao próximo leitor elegível quando uma devolução antecipada permitir a retirada antes da data inicialmente reservada.

## Benefício esperado
Antecipar o acesso ao livro e melhorar o aproveitamento do acervo sem retirar do leitor a data final já organizada.

## Alinhamento com o projeto
A capacidade complementa a fila de espera e a política de antecipação por devolução, mas não é necessária para validar a primeira versão do fluxo principal.

## Fluxo esperado
1. Um exemplar é devolvido antes da data prevista.
2. O sistema identifica o próximo leitor elegível na fila.
3. O sistema envia uma notificação por e-mail informando a disponibilidade antecipada.
4. O leitor pode retirar o exemplar antes da data reservada conforme as regras vigentes.
5. A data final originalmente reservada é preservada, mesmo que isso gere a exceção aprovada ao período máximo normal.

## Escopo inicial
- Notificação por e-mail para disponibilidade antecipada causada por devolução antes do prazo.
- Identificação do próximo leitor elegível.

## Fora de escopo
- Implementação na primeira versão.
- Definição antecipada do provedor de e-mail.
- Outros tipos de notificação.

## Critérios iniciais de sucesso
- O e-mail é enviado somente ao próximo leitor elegível.
- A mensagem informa de forma compreensível que a retirada pode ser antecipada.
- Nenhuma notificação altera silenciosamente as datas confirmadas.

## Dependências
- Fila de espera implementada e validada.
- Registro de devolução antecipada.
- Endereço de e-mail válido do leitor.
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
