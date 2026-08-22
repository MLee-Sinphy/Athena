# GLOSSARY.md

> Vocabulário oficial do domínio Athena.

## Leitor
### Definição
Pessoa cadastrada pela instituição que pode consultar o acervo e solicitar empréstimos.
### Exemplo
Aluno, universitário ou usuário de biblioteca pública.
### Não confundir com
Administrador ou dispositivo físico de leitura.
### Observações
É o nome neutro adotado no produto, independentemente do tipo de instituição.
### Referências relacionadas
`PROJECT.md`, `REQUIREMENTS.md`.

## Administrador
### Definição
Pessoa autorizada a gerenciar leitores, acervo, políticas e operações.
### Exemplo
Bibliotecário ou coordenador atuando no perfil administrativo.
### Não confundir com
Administrador da infraestrutura do VPS.
### Observações
Intervenções relevantes geram auditoria.
### Referências relacionadas
`REQUIREMENTS.md`.

## Título
### Definição
Registro bibliográfico que agrupa exemplares equivalentes de uma obra e edição.
### Exemplo
Uma edição específica de um romance exibida uma vez no catálogo.
### Não confundir com
Exemplar físico.
### Observações
Recebe descrição, tags e média de conteúdo.
### Referências relacionadas
`REQUIREMENTS.md`, `ARCHITECTURE.md`.

## Exemplar
### Definição
Cópia física individual de um título, identificada por código único.
### Exemplo
A cópia `EX-0042`, com estado de conservação próprio.
### Não confundir com
Título agregado no catálogo.
### Observações
Recebe estado operacional e média de conservação.
### Referências relacionadas
`REQUIREMENTS.md`.

## Reserva
### Definição
Direito confirmado de usar um exemplar em um intervalo futuro, ainda sem retirada física.
### Exemplo
Reserva de 10 a 17 de setembro.
### Não confundir com
Empréstimo ativo.
### Observações
Só se torna empréstimo quando a retirada é confirmada.
### Referências relacionadas
`REQUIREMENTS.md`.

## Empréstimo
### Definição
Operação iniciada pela confirmação da retirada física de um exemplar.
### Exemplo
Exemplar retirado em 10 de setembro e previsto para devolução em 17 de setembro.
### Não confundir com
Solicitação ou reserva.
### Observações
Permanece ativo até devolução, perda ou encerramento administrativo aplicável.
### Referências relacionadas
`REQUIREMENTS.md`.

## Fila de espera
### Definição
Ordem cronológica de solicitações concorrentes por um título sem disponibilidade no período desejado.
### Exemplo
O primeiro pedido elegível recebe prioridade sobre a próxima oportunidade.
### Não confundir com
Lista pública de leitores; identidades nunca são expostas.
### Observações
Também chamada fila FIFO.
### Referências relacionadas
`REQUIREMENTS.md`.

## Dia de funcionamento
### Definição
Data em que a biblioteca está aberta conforme semana regular, feriados e fechamentos configurados.
### Exemplo
Uma segunda-feira não marcada como feriado.
### Não confundir com
Dia corrido usado em penalidades explícitas.
### Observações
Prazos de reserva e empréstimo usam este calendário.
### Referências relacionadas
`REQUIREMENTS.md`.

## Tolerância de retirada
### Definição
Período após a data marcada durante o qual o leitor conserva exclusividade para retirar.
### Exemplo
Um dia de funcionamento por padrão.
### Não confundir com
Prazo total do empréstimo.
### Observações
Após a tolerância, a reserva não é cancelada imediatamente, mas o intervalo pode ser ocupado por outra pessoa.
### Referências relacionadas
`REQUIREMENTS.md`.

## Tag
### Definição
Palavra-chave pesquisável que caracteriza um título.
### Exemplo
`#medieval`.
### Não confundir com
Categoria bibliográfica única.
### Observações
Leitores podem sugerir tags após devolver; autoria e data são preservadas.
### Referências relacionadas
`REQUIREMENTS.md`.

## Aviso interno
### Definição
Mensagem persistente exibida ao usuário autenticado dentro do Athena.
### Exemplo
Disponibilidade antecipada apresentada no próximo acesso.
### Não confundir com
E-mail, que é futuro.
### Observações
Eventos relevantes registram leitura e resposta quando aplicável.
### Referências relacionadas
`REQUIREMENTS.md`, `FEATURES.md`.

## Estado de conservação
### Definição
Avaliação do estado físico do exemplar, derivada das notas dos leitores.
### Exemplo
Média de 4,2 estrelas.
### Não confundir com
Estado operacional como disponível ou danificado.
### Observações
Pode orientar a escolha do exemplar.
### Referências relacionadas
`REQUIREMENTS.md`.

## Penalidade
### Definição
Restrição aplicada ao leitor por atraso ou cancelamentos frequentes.
### Exemplo
Bloqueio de novas solicitações por sete dias corridos.
### Não confundir com
Cancelamento administrativo de uma operação específica.
### Observações
Parâmetros são configuráveis.
### Referências relacionadas
`REQUIREMENTS.md`.

## Auditoria
### Definição
Histórico imutável de ações administrativas relevantes.
### Exemplo
Alteração de devolução com autor, horário, valor anterior e novo.
### Não confundir com
Log técnico de aplicação.
### Observações
Justificativa é opcional.
### Referências relacionadas
`REQUIREMENTS.md`, `ARCHITECTURE.md`.
