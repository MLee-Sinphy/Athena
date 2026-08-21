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

---

# FEATURE-002 — Recuperação autônoma de senha por e-mail

## Estado
- [x] Adiada

## Origem
- Usuário: contexto fornecido pelo responsável em 2026-08-21.

## Problema ou oportunidade
Na primeira versão, o sistema não enviará e-mails e a recuperação de acesso dependerá da assistência de um administrador.

## Público beneficiado
Leitores e administradores que esquecerem suas senhas.

## Proposta
Permitir que o usuário solicite autonomamente a recuperação da senha por meio de uma mensagem enviada ao e-mail cadastrado.

## Benefício esperado
Reduzir a dependência de administradores e permitir recuperação segura de acesso sem intervenção manual.

## Alinhamento com o projeto
A capacidade complementa a autenticação, mas depende da infraestrutura de e-mail que foi deliberadamente adiada.

## Fluxo esperado
1. O usuário informa seu e-mail ou identificador na recuperação de acesso.
2. O sistema responde sem revelar se a conta existe.
3. Quando aplicável, o sistema envia um token de uso único e curta duração ao e-mail cadastrado.
4. O usuário define uma nova senha válida.
5. O token é invalidado e as sessões anteriores aplicáveis são encerradas.

## Escopo inicial
- Solicitação de recuperação.
- Token aleatório, de uso único e com expiração.
- Definição de nova senha.
- Invalidação segura do token e das sessões aplicáveis.

## Fora de escopo
- Implementação na primeira versão.
- Escolha antecipada do provedor de e-mail.
- Recuperação por perguntas de segurança.

## Critérios iniciais de sucesso
- A resposta pública não permite descobrir se uma conta existe.
- Tokens expiram, são de uso único e não são armazenados em texto puro.
- A nova senha respeita a política vigente.
- Sessões anteriores aplicáveis são invalidadas depois da recuperação.

## Dependências
- Serviço de envio de e-mail ainda não escolhido.
- E-mail válido e único no contexto da instituição.
- Autenticação e gestão de sessões implementadas.

## Riscos
- Enumeração de contas.
- Roubo ou reutilização de token.
- Entrega atrasada ou falha do provedor de e-mail.

## Impactos possíveis
- Produto: oferece recuperação sem administrador.
- UX/UI: exige telas de solicitação e redefinição.
- Arquitetura: exige tokens temporários e integração de e-mail.
- Dados: exige armazenar estado seguro e expiração da solicitação.
- Segurança: exige limitação de frequência, respostas neutras e invalidação.
- Desempenho: o envio não deve bloquear a resposta principal.
- Documentação: requisitos, arquitetura, UX/UI, testes e decisões serão atualizados quando a feature for priorizada.

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
