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

# FEATURE-001 — E-mails de disponibilidade antecipada

## Estado
- [x] Adiada

## Origem
- Usuário: contexto fornecido pelo responsável em 2026-08-20.

## Problema ou oportunidade
Avisos internos de disponibilidade antecipada fazem parte da primeira versão, mas o leitor só os vê ao acessar o sistema.

## Público beneficiado
Leitores que aguardam um exemplar já reservado para um período futuro.

## Proposta
Enviar por e-mail o aviso já registrado internamente quando uma devolução antecipada ou a perda de exclusividade liberar o exemplar.

## Benefício esperado
Antecipar o acesso ao livro e melhorar o aproveitamento do acervo sem retirar do leitor a data final já organizada.

## Alinhamento com o projeto
A capacidade complementa o aviso interno da primeira versão e reduz a dependência de acesso frequente ao sistema.

## Fluxo esperado
1. Um exemplar é devolvido antes da data prevista.
2. O sistema identifica o próximo leitor elegível na fila.
3. O sistema cria o aviso interno da primeira versão e agenda o e-mail correspondente.
4. O sistema registra a tentativa e o resultado do envio; leitura, aceite e recusa permanecem associados ao aviso interno.
5. O leitor pode aceitar ou recusar a antecipação até a data original de início de sua reserva.
6. Se aceitar, pode retirar o exemplar antes da data reservada conforme as regras vigentes.
7. Se recusar, preserva integralmente sua reserva original.
8. A data final originalmente reservada é preservada, mesmo que isso gere a exceção aprovada ao período máximo normal.

## Escopo inicial
- E-mail para disponibilidade antecipada causada por devolução antes do prazo ou reserva não retirada.
- Registro da tentativa, do provedor e do resultado do envio.

## Fora de escopo
- Implementação na primeira versão.
- Definição antecipada do provedor de e-mail.
- Aviso interno, já incluído na primeira versão por REQ-F-014.
- E-mails não relacionados à disponibilidade antecipada.

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
- Avisos internos implementados e validados.
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
- Roadmap: horizonte futuro sem versão aprovada.
- Requisito: Pendente.
- Decisão: Pendente.
- Tarefa: Pendente.

## Resultado
- Versão entregue: Não entregue.
- Data: Não aplicável.

---

# FEATURE-003 — Retirada e devolução assistidas por leitor físico

## Estado
- [x] Adiada

## Origem
- Usuário: contexto fornecido pelo responsável em 2026-08-22.

## Problema ou oportunidade
A primeira versão registra digitalmente operações cuja entrega e devolução continuam sendo confirmadas pela interação convencional com a biblioteca. Uma integração física futura pode tornar essas operações mais rápidas e autônomas.

## Público beneficiado
Leitores e equipes administrativas de bibliotecas que adotarem equipamentos compatíveis.

## Proposta
Permitir que o leitor se identifique e escaneie o exemplar físico para registrar sua retirada ou devolução, respeitando as mesmas regras, permissões, períodos e registros de auditoria da API.

## Benefício esperado
Reduzir trabalho operacional, diminuir erros de identificação do exemplar e oferecer autoatendimento controlado.

## Alinhamento com o projeto
A capacidade estende o controle individual de exemplares e reutiliza o domínio de reservas e empréstimos, sem alterar as regras centrais.

## Fluxo esperado
1. O leitor autentica ou identifica-se no dispositivo autorizado.
2. O dispositivo lê o identificador único do exemplar.
3. A integração solicita à API a retirada ou a devolução.
4. A API autentica o dispositivo e o leitor, valida as regras e executa ou rejeita a operação.
5. O resultado é apresentado ao leitor e registrado na auditoria.

## Escopo inicial
- Contrato de integração para identificação do leitor e do exemplar.
- Retirada e devolução por dispositivo autorizado.
- Aplicação integral das regras existentes.
- Auditoria do leitor, dispositivo, exemplar, operação e resultado.

## Fora de escopo
- Implementação na primeira versão.
- Escolha antecipada entre código de barras, QR Code, RFID ou outra tecnologia.
- Compra, instalação ou manutenção de hardware.
- Alteração das regras de empréstimo para acomodar limitações de um fornecedor específico.

## Critérios iniciais de sucesso
- O dispositivo não consegue ignorar autenticação, autorização ou regras de negócio.
- O exemplar correto é associado à operação.
- Operações duplicadas ou concorrentes não geram estados inconsistentes.
- Falhas de comunicação não produzem falsa confirmação de retirada ou devolução.
- Toda tentativa relevante possui registro auditável.

## Dependências
- API estável para reservas, empréstimos e devoluções.
- Identificador físico legível e único em cada exemplar.
- Mecanismo de autenticação para dispositivos.
- Hardware e protocolo ainda não escolhidos.

## Riscos
- Duplicação de operação causada por repetição de leitura.
- Uso indevido de dispositivo ou identificador.
- Incompatibilidade entre fornecedores.
- Operação física concluída enquanto a API está indisponível.

## Impactos possíveis
- Produto: acrescenta autoatendimento.
- UX/UI: exige interface adequada ao dispositivo e feedback imediato.
- Arquitetura: exige API idempotente e autenticação de dispositivos.
- Dados: exige identificar dispositivo e origem da operação.
- Segurança: amplia a superfície física e lógica de autenticação.
- Desempenho: exige resposta rápida durante leitura presencial.
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
