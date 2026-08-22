# REQUIREMENTS.md

> Fonte oficial de casos de uso, requisitos e regras. IDs são estáveis e relações aparecem por referências cruzadas.

## Convenções

- Estados: Proposto, Aprovado, Implementado, Verificado ou Rejeitado.
- Prioridades não funcionais: Obrigatória, Alta, Média ou Baixa.
- Casos de uso: `UC-[ID]`; funcionais: `REQ-F-[ID]`; não funcionais: `REQ-NF-[ID]`; regras: `RULE-[ID]`.
- Todos os itens abaixo estão **Propostos** até a validação humana integral desta documentação.

# Casos de uso

## UC-001 — Autenticar e administrar o próprio acesso
### Estado
Proposto.
### Ator principal
Leitor ou administrador.
### Atores secundários
Administrador, na criação e recuperação assistida.
### Objetivo
Entrar com e-mail ou matrícula, trocar senha temporária e manter credenciais próprias.
### Pré-condições
Conta criada pelo administrador.
### Gatilho
Usuário abre o login ou uma função de credenciais.
### Fluxo principal
1. Informa identificador e senha. 2. Sistema valida e cria sessão. 3. Se a senha for temporária, exige troca antes das demais funções.
### Fluxos alternativos
Administrador redefine o acesso com nova senha temporária; usuário autenticado altera e-mail ou senha.
### Exceções
Credenciais inválidas, conta impedida, limite de tentativas ou backend indisponível.
### Pós-condições
Sessão válida ou falha neutra e segura.
### Requisitos funcionais envolvidos
REQ-F-001, REQ-F-002, REQ-F-003.
### Regras de negócio aplicáveis
RULE-001, RULE-002.
### Requisitos não funcionais relevantes
REQ-NF-001, REQ-NF-002, REQ-NF-003.

## UC-002 — Consultar o catálogo
### Estado
Proposto.
### Ator principal
Leitor.
### Objetivo
Localizar títulos, consultar disponibilidade e comparar exemplares por conservação.
### Pré-condições
Catálogo acessível.
### Gatilho
Leitor abre ou pesquisa o catálogo.
### Fluxo principal
1. Pesquisa ou filtra. 2. Sistema retorna títulos agrupados. 3. Leitor abre detalhes e, quando relevante, compara exemplares disponíveis.
### Fluxos alternativos
Consulta sem filtros ou resultado vazio.
### Exceções
Backend indisponível.
### Pós-condições
Nenhuma alteração de domínio.
### Requisitos funcionais envolvidos
REQ-F-004, REQ-F-005.
### Regras de negócio aplicáveis
RULE-003.
### Requisitos não funcionais relevantes
REQ-NF-004, REQ-NF-005, REQ-NF-006.

## UC-003 — Solicitar reserva
### Estado
Proposto.
### Ator principal
Leitor.
### Objetivo
Reservar um título para um intervalo permitido.
### Pré-condições
Leitor autenticado e elegível.
### Gatilho
Escolha de título, exemplar opcional e datas.
### Fluxo principal
1. Sistema valida calendário, limite, penalidades e disponibilidade. 2. Associa exemplar compatível. 3. Confirma a reserva sem aprovação administrativa.
### Fluxos alternativos
Sem disponibilidade, oferece período futuro e fila FIFO.
### Exceções
Conflito concorrente ou regra impeditiva gera recusa explicada.
### Pós-condições
Reserva confirmada ou solicitação recusada sem alteração parcial.
### Requisitos funcionais envolvidos
REQ-F-006, REQ-F-007, REQ-F-008.
### Regras de negócio aplicáveis
RULE-004 a RULE-008.
### Requisitos não funcionais relevantes
REQ-NF-007, REQ-NF-008.

## UC-004 — Retirar e devolver exemplar
### Estado
Proposto.
### Ator principal
Administrador, registrando a operação física do leitor.
### Objetivo
Converter reserva em empréstimo e concluir a devolução do exemplar correto.
### Pré-condições
Reserva válida para retirada ou empréstimo ativo para devolução.
### Gatilho
Apresentação física do leitor e exemplar.
### Fluxo principal
1. Administrador confirma retirada. 2. Reserva vira empréstimo. 3. Na devolução, sistema encerra o empréstimo e atualiza disponibilidade.
### Fluxos alternativos
Retirada atrasada ainda permitida enquanto não houver conflito; devolução antecipada libera oportunidade.
### Exceções
Exemplar incorreto, conflito ou operação já concluída.
### Pós-condições
Estado consistente e evento histórico preservado.
### Requisitos funcionais envolvidos
REQ-F-009, REQ-F-010, REQ-F-011.
### Regras de negócio aplicáveis
RULE-009, RULE-010.
### Requisitos não funcionais relevantes
REQ-NF-007, REQ-NF-009.

## UC-005 — Administrar reserva ou empréstimo próprio
### Estado
Proposto.
### Ator principal
Leitor.
### Objetivo
Alterar, cancelar ou renovar quando permitido.
### Pré-condições
Operação pertencente ao leitor.
### Gatilho
Ação na área pessoal.
### Fluxo principal
Antes da retirada, altera datas ou cancela sem conflito; depois, altera apenas devolução sem fila e dentro do máximo.
### Fluxos alternativos
Sistema explica impedimento e preserva estado anterior.
### Exceções
Concorrência ou operação em estado incompatível.
### Pós-condições
Operação alterada de forma atômica ou inalterada.
### Requisitos funcionais envolvidos
REQ-F-012, REQ-F-013.
### Regras de negócio aplicáveis
RULE-011, RULE-012.
### Requisitos não funcionais relevantes
REQ-NF-007.

## UC-006 — Receber e responder aviso interno
### Estado
Proposto.
### Ator principal
Leitor.
### Objetivo
Conhecer antecipação ou perda de intervalo e responder quando aplicável.
### Pré-condições
Evento relevante registrado.
### Gatilho
Login ou abertura da área de avisos.
### Fluxo principal
Sistema exibe aviso não lido; leitor lê e aceita ou recusa antecipação.
### Fluxos alternativos
Aviso apenas informativo sobre ocupação do período perdido.
### Exceções
Prazo de resposta expirado.
### Pós-condições
Leitura e resposta registradas; reserva original preservada quando a antecipação for recusada.
### Requisitos funcionais envolvidos
REQ-F-014.
### Regras de negócio aplicáveis
RULE-010.
### Requisitos não funcionais relevantes
REQ-NF-005, REQ-NF-009.

## UC-007 — Avaliar e sugerir tags
### Estado
Proposto.
### Ator principal
Leitor.
### Objetivo
Registrar percepção após uma devolução concluída.
### Pré-condições
Empréstimo do leitor devolvido.
### Gatilho
Leitor abre a avaliação.
### Fluxo principal
Informa opcionalmente notas de 1 a 5 para conteúdo e conservação e sugere tags.
### Fluxos alternativos
Envia apenas parte dos campos opcionais.
### Exceções
Tentativa de editar avaliação enviada ou avaliar empréstimo alheio.
### Pós-condições
Dados individuais e autoria das tags preservados; médias atualizáveis.
### Requisitos funcionais envolvidos
REQ-F-015.
### Regras de negócio aplicáveis
RULE-013.
### Requisitos não funcionais relevantes
REQ-NF-009.

## UC-008 — Administrar usuários e acervo
### Estado
Proposto.
### Ator principal
Administrador.
### Objetivo
Manter leitores, títulos e exemplares.
### Pré-condições
Administrador autenticado.
### Gatilho
Ação no painel.
### Fluxo principal
Cadastra ou altera dados válidos e recebe confirmação.
### Fluxos alternativos
Redefine senha temporária ou restaura estado de exemplar.
### Exceções
Duplicidade, dado inválido ou transição conflitante.
### Pós-condições
Dados persistidos e ações relevantes auditadas.
### Requisitos funcionais envolvidos
REQ-F-002, REQ-F-016.
### Regras de negócio aplicáveis
RULE-001, RULE-003, RULE-014.
### Requisitos não funcionais relevantes
REQ-NF-001, REQ-NF-009.

## UC-009 — Configurar calendário e políticas
### Estado
Proposto.
### Ator principal
Administrador.
### Objetivo
Adaptar funcionamento, limites e penalidades da instituição.
### Pré-condições
Administrador autenticado.
### Gatilho
Alteração no painel de políticas.
### Fluxo principal
Sistema valida, salva e audita nova configuração, aplicada somente conforme sua vigência.
### Fluxos alternativos
Suspende novas reservas preservando as confirmadas.
### Exceções
Intervalos ou valores incoerentes.
### Pós-condições
Política versionada e consultável.
### Requisitos funcionais envolvidos
REQ-F-017.
### Regras de negócio aplicáveis
RULE-005, RULE-006, RULE-012, RULE-015.
### Requisitos não funcionais relevantes
REQ-NF-009.

## UC-010 — Consultar e intervir administrativamente
### Estado
Proposto.
### Ator principal
Administrador.
### Objetivo
Consultar histórico e alterar ou cancelar operações.
### Pré-condições
Administrador autenticado.
### Gatilho
Seleção de operação ou auditoria.
### Fluxo principal
Visualiza dados, executa intervenção e sistema registra antes/depois, autor e horário.
### Fluxos alternativos
Adiciona justificativa opcional.
### Exceções
Conflito impede alteração inconsistente.
### Pós-condições
Operação consistente e trilha imutável.
### Requisitos funcionais envolvidos
REQ-F-018, REQ-F-019.
### Regras de negócio aplicáveis
RULE-014, RULE-015.
### Requisitos não funcionais relevantes
REQ-NF-001, REQ-NF-009.

# Requisitos funcionais

## REQ-F-001 — Autenticar por e-mail ou matrícula
### Estado
Proposto.
### Descrição
Validar um único identificador e senha e emitir sessão segura.
### Objetivo
Oferecer acesso uniforme aos dois perfis.
### Pré-condições
Conta existente.
### Entradas
Identificador e senha.
### Saídas
Sessão ou erro neutro.
### Critérios de aceitação
- Ambos os identificadores funcionam; credencial inválida não revela existência da conta; limitação de tentativas é aplicada.
### Casos de uso relacionados
UC-001.
### Regras de negócio aplicáveis
RULE-001, RULE-002.
### Requisitos não funcionais relacionados
REQ-NF-001 a REQ-NF-003.

## REQ-F-002 — Gerenciar primeiro acesso e recuperação assistida
### Estado
Proposto.
### Descrição
Exigir troca da senha temporária e permitir que administrador emita outra.
### Critérios de aceitação
- Senha temporária bloqueia funções comuns; troca válida invalida credenciais anteriores; não há e-mail na v1.
### Casos de uso relacionados
UC-001, UC-008.
### Regras de negócio aplicáveis
RULE-001, RULE-002.

## REQ-F-003 — Alterar credenciais próprias e encerrar sessão
### Estado
Proposto.
### Descrição
Permitir alteração de e-mail e senha e logout.
### Critérios de aceitação
- Unicidade é validada; troca de senha e logout invalidam sessões aplicáveis.
### Casos de uso relacionados
UC-001.

## REQ-F-004 — Exibir catálogo agrupado
### Estado
Proposto.
### Descrição
Exibir cada título uma vez, com disponibilidade agregada e detalhes bibliográficos.
### Critérios de aceitação
- Códigos internos não aparecem na listagem; dados de outros leitores nunca aparecem.
### Casos de uso relacionados
UC-002.

## REQ-F-005 — Pesquisar, filtrar e comparar exemplares
### Estado
Proposto.
### Descrição
Pesquisar campos bibliográficos, descrição completa e tags; filtrar e comparar conservação de exemplares disponíveis.
### Critérios de aceitação
- `#medieval` encontra a tag correspondente; termos da descrição são encontrados; ISBN ausente não impede cadastro.
### Casos de uso relacionados
UC-002.

## REQ-F-006 — Validar e conceder reserva
### Estado
Proposto.
### Descrição
Avaliar regras e conceder automaticamente reserva válida, associando exemplar escolhido ou compatível.
### Critérios de aceitação
- Concessão é atômica; recusa identifica o impedimento; nenhuma confirmação administrativa é exigida.
### Casos de uso relacionados
UC-003.

## REQ-F-007 — Calcular calendário e disponibilidade futura
### Estado
Proposto.
### Descrição
Considerar dias regulares, feriados, fechamentos e períodos dos exemplares.
### Critérios de aceitação
- Dias fechados não contam no prazo; nenhuma sobreposição confirmada é criada.
### Casos de uso relacionados
UC-003.

## REQ-F-008 — Organizar fila FIFO privada
### Estado
Proposto.
### Descrição
Ordenar solicitações elegíveis pelo instante de criação e mostrar somente posição e estimativas próprias.
### Critérios de aceitação
- Empates usam identificador monotônico; nenhuma identidade alheia é exposta.
### Casos de uso relacionados
UC-003.

## REQ-F-009 — Confirmar retirada física
### Estado
Proposto.
### Descrição
Converter a reserva em empréstimo ativo somente na confirmação do exemplar físico.
### Critérios de aceitação
- Data/hora e exemplar são registrados; repetição não duplica empréstimo.
### Casos de uso relacionados
UC-004.

## REQ-F-010 — Confirmar devolução e liberar exemplar
### Estado
Proposto.
### Descrição
Encerrar empréstimo, registrar data e recalcular oportunidades.
### Critérios de aceitação
- Devolução é idempotente; atraso ou antecipação é identificado; histórico permanece.
### Casos de uso relacionados
UC-004.

## REQ-F-011 — Tratar retirada não realizada
### Estado
Proposto.
### Descrição
Remover exclusividade após a tolerância sem cancelar imediatamente e permitir ocupação do intervalo livre.
### Critérios de aceitação
- Leitor original retira se ainda não houver conflito; ao surgir conflito recebe aviso e deve escolher novas datas.
### Casos de uso relacionados
UC-004, UC-006.

## REQ-F-012 — Alterar ou cancelar reserva própria
### Estado
Proposto.
### Descrição
Permitir mudanças anteriores à retirada sem afetar períodos confirmados.
### Critérios de aceitação
- Cancelamento entra na janela aplicável; alteração conflitante é rejeitada atomicamente.
### Casos de uso relacionados
UC-005.

## REQ-F-013 — Renovar empréstimo
### Estado
Proposto.
### Descrição
Alterar somente a devolução quando não houver fila e o máximo for respeitado.
### Critérios de aceitação
- Início não muda; fila ou excesso de prazo impede renovação.
### Casos de uso relacionados
UC-005.

## REQ-F-014 — Exibir avisos internos
### Estado
Proposto.
### Descrição
Exibir ao entrar avisos de antecipação e perda do intervalo, registrando leitura e resposta aplicável.
### Critérios de aceitação
- Próximo elegível pode aceitar ou recusar até sua data original; recusa preserva reserva; e-mail não é necessário.
### Casos de uso relacionados
UC-006.

## REQ-F-015 — Registrar avaliações e tags sugeridas
### Estado
Proposto.
### Descrição
Após devolução, aceitar notas opcionais de 1 a 5 e tags, preservando autoria e data.
### Critérios de aceitação
- Somente responsável pelo empréstimo avalia; avaliação enviada não é editável; médias derivam dos registros individuais.
### Casos de uso relacionados
UC-007.

## REQ-F-016 — Gerenciar leitores, títulos e exemplares
### Estado
Proposto.
### Descrição
Oferecer CRUD administrativo com validação, estados e códigos únicos.
### Critérios de aceitação
- Campos obrigatórios são validados; ISBN é opcional; restaurações de estado são auditadas.
### Casos de uso relacionados
UC-008.

## REQ-F-017 — Configurar calendário e políticas
### Estado
Proposto.
### Descrição
Gerenciar dias, fechamentos, prazos, limites, tolerância, penalidades, renovação e suspensão.
### Critérios de aceitação
- Padrões oficiais são inicializados; alteração não cancela silenciosamente reservas existentes; configuração é auditada.
### Casos de uso relacionados
UC-009.

## REQ-F-018 — Intervir em operações
### Estado
Proposto.
### Descrição
Permitir que administrador visualize, altere ou cancele qualquer reserva ou empréstimo de modo consistente.
### Critérios de aceitação
- Toda intervenção relevante é auditada; conflitos são recusados.
### Casos de uso relacionados
UC-010.

## REQ-F-019 — Consultar auditoria e histórico
### Estado
Proposto.
### Descrição
Consultar eventos administrativos e históricos necessários a rastreabilidade e análises futuras.
### Critérios de aceitação
- Auditoria contém autor, horário, ação, antes/depois e justificativa opcional; registros comuns não podem alterá-la.
### Casos de uso relacionados
UC-010.

## REQ-F-020 — Informar indisponibilidade do backend
### Estado
Proposto.
### Descrição
Informar falha de acesso à API sem apresentar a operação como concluída.
### Critérios de aceitação
- Mensagem compreensível, sem detalhes internos, oferece nova tentativa quando aplicável e nunca mostra sucesso indevido.
### Casos de uso relacionados
Todos os casos que dependem da API.

# Requisitos não funcionais

## REQ-NF-001 — Autorização por perfil e propriedade
### Categoria
Segurança.
### Estado
Proposto.
### Regra
Backend autoriza toda operação por perfil, propriedade e estado; frontend não é fronteira de segurança.
### Critério de verificação
Testes de matriz de permissões e IDOR.
### Prioridade
Obrigatória.

## REQ-NF-002 — Política de senha
### Categoria
Segurança.
### Estado
Proposto.
### Regra
Mínimo 15 caracteres, aceitar ao menos 64, espaços e Unicode normalizado; bloquear senhas comuns/comprometidas, sem composição artificial.
### Critério de verificação
Testes de validadores e hash seguro do Django.
### Prioridade
Obrigatória.

## REQ-NF-003 — Sessão e token
### Categoria
Segurança.
### Estado
Proposto.
### Regra
Token opaco revogável somente em memória; 30 minutos de inatividade e 8 horas absolutas; CORS restrito e HTTPS.
### Critério de verificação
Testes de expiração, revogação, storage, cabeçalhos e CORS.
### Prioridade
Obrigatória.

## REQ-NF-004 — Responsividade e compatibilidade
### Categoria
Usabilidade.
### Estado
Proposto.
### Regra
Todas as funções essenciais operam em smartphone e computador nas duas versões estáveis mais recentes dos navegadores definidos.
### Critério de verificação
Matriz de viewports e navegadores.
### Prioridade
Obrigatória.

## REQ-NF-005 — Acessibilidade
### Categoria
Acessibilidade.
### Estado
Proposto.
### Regra
Atender critérios aplicáveis da WCAG 2.2 AA.
### Critério de verificação
Automação e revisão manual de teclado, foco, contraste, semântica, leitor de tela e reflow.
### Prioridade
Obrigatória.

## REQ-NF-006 — Internacionalização
### Categoria
Usabilidade.
### Estado
Proposto.
### Regra
Interface em pt-BR e en, inicializada pelo navegador e alterável manualmente sem geolocalização por IP.
### Critério de verificação
Testes nos dois catálogos de mensagens e persistência da preferência.
### Prioridade
Alta.

## REQ-NF-007 — Integridade e concorrência
### Categoria
Confiabilidade.
### Estado
Proposto.
### Regra
Operações críticas são transacionais, idempotentes quando repetíveis e impedem sobreposição de exemplar.
### Critério de verificação
Testes concorrentes reais em PostgreSQL.
### Prioridade
Obrigatória.

## REQ-NF-008 — Escala simulada
### Categoria
Desempenho.
### Estado
Proposto.
### Regra
Projetar e simular 5.000 leitores, 20.000 títulos, 50.000 exemplares e pico de 500 usuários simultâneos.
### Critério de verificação
Teste de carga reproduzível com resultados e limitações registrados.
### Prioridade
Alta.

## REQ-NF-009 — Retenção, auditoria e privacidade
### Categoria
Dados.
### Estado
Proposto.
### Regra
Preservar históricos e autoria necessários, anonimizar quando aplicável e impedir exposição de outros leitores.
### Critério de verificação
Testes de retenção, anonimização, imutabilidade e serialização por perfil.
### Prioridade
Obrigatória.

## REQ-NF-010 — Backup restaurável
### Categoria
Operação.
### Estado
Proposto.
### Regra
Backup conjunto de banco e imagens, criptografado fora do VPS, com 7 diárias, 4 semanais e restauração testada antes de entregas relevantes.
### Critério de verificação
Registro de checksum e exercício de restauração.
### Prioridade
Alta.

## REQ-NF-011 — Observabilidade segura
### Categoria
Operação.
### Estado
Proposto.
### Regra
Logs estruturados e correlacionáveis para erros, autenticação e operações relevantes, sem segredos nem dados pessoais desnecessários.
### Critério de verificação
Inspeção automatizada e cenário ponta a ponta por identificador de correlação.
### Prioridade
Alta.

## REQ-NF-012 — Temas por tokens
### Categoria
Manutenibilidade e UX.
### Estado
Proposto.
### Regra
Cores e efeitos usam tokens semânticos, seis temas selecionáveis centralmente e fallback opaco no Aqua Glass.
### Critério de verificação
Inspeção de estilos e testes de contraste em todos os temas.
### Prioridade
Média.

# Regras de negócio

## RULE-001 — Cadastro institucional
### Estado
Proposto.
### Regra
Somente administrador cria leitores; matrícula e e-mail são únicos na instituição.
### Exceções
Nenhuma na v1.
### Validação
Constraints no banco e validação da API.
### Requisitos relacionados
REQ-F-001, REQ-F-002, REQ-F-016.

## RULE-002 — Primeiro acesso e senha
### Estado
Proposto.
### Regra
Senha inicial ou redefinida é temporária e deve ser trocada antes do uso comum.
### Exceções
Administrador pode emitir nova senha temporária.
### Validação
Estado da credencial verificado pelo backend.
### Requisitos relacionados
REQ-F-001 a REQ-F-003.

## RULE-003 — Título e exemplar
### Estado
Proposto.
### Regra
Catálogo agrupa por título; exemplar tem código único, estado e conservação próprios; leitor pode escolhê-lo pela conservação.
### Exceções
Sem escolha, sistema associa exemplar compatível.
### Validação
Modelo relacional e resposta por perfil.
### Requisitos relacionados
REQ-F-004, REQ-F-005, REQ-F-016.

## RULE-004 — Reserva obrigatória
### Estado
Proposto.
### Regra
Todo empréstimo começa por reserva e só se torna ativo na retirada física.
### Exceções
Nenhuma na v1.
### Validação
Máquina de estados.
### Requisitos relacionados
REQ-F-006, REQ-F-009.

## RULE-005 — Calendário
### Estado
Proposto.
### Regra
Prazos contam somente dias de funcionamento configurados; padrão segunda a sexta, mínimo 3 e máximo 15.
### Exceções
Penalidades declaradas em dias corridos.
### Validação
Serviço de calendário e testes de borda.
### Requisitos relacionados
REQ-F-007, REQ-F-017.

## RULE-006 — Limite simultâneo
### Estado
Proposto.
### Regra
Padrão de 3 empréstimos simultâneos, configurável e redutível por penalidade.
### Exceções
Reservas confirmadas não são canceladas automaticamente.
### Validação
Contagem transacional na concessão e retirada.
### Requisitos relacionados
REQ-F-006, REQ-F-017.

## RULE-007 — Não sobreposição
### Estado
Proposto.
### Regra
Um exemplar não pode possuir períodos confirmados sobrepostos.
### Exceções
Nenhuma.
### Validação
Transação, bloqueio e teste concorrente.
### Requisitos relacionados
REQ-F-006, REQ-F-007.

## RULE-008 — Prioridade FIFO
### Estado
Proposto.
### Regra
Solicitação elegível mais antiga tem prioridade; a ordem não muda silenciosamente.
### Exceções
Perda de exclusividade após tolerância conforme RULE-010.
### Validação
Ordenação por instante e desempate monotônico.
### Requisitos relacionados
REQ-F-008.

## RULE-009 — Estado do empréstimo
### Estado
Proposto.
### Regra
Reserva confirmada não é empréstimo ativo até a retirada; devolução encerra o empréstimo.
### Exceções
Encerramentos administrativos precisam de auditoria.
### Validação
Transições autorizadas.
### Requisitos relacionados
REQ-F-009, REQ-F-010.

## RULE-010 — Tolerância e oportunidade antecipada
### Estado
Proposto.
### Regra
Após 1 dia de funcionamento por padrão, o ausente perde exclusividade, mas retira enquanto livre; próximo pode antecipar mantendo a devolução original; conflito posterior desloca o ausente e gera aviso.
### Exceções
Antecipação pode exceder o máximo normal.
### Validação
Serviço de disponibilidade, aviso e teste de concorrência.
### Requisitos relacionados
REQ-F-011, REQ-F-014.

## RULE-011 — Alterações pelo leitor
### Estado
Proposto.
### Regra
Antes da retirada, ambas as datas podem mudar sem conflito; depois, somente devolução, sem fila e dentro do máximo.
### Exceções
Administrador possui intervenção auditada.
### Validação
Estado, propriedade e disponibilidade.
### Requisitos relacionados
REQ-F-012, REQ-F-013.

## RULE-012 — Penalidades
### Estado
Proposto.
### Regra
Atraso bloqueia novas reservas e empréstimos por 7 dias corridos; mais de 3 cancelamentos numa janela de 30 dias bloqueia novas solicitações até seu fim.
### Exceções
Parâmetros configuráveis; cancelamentos administrativos não contam; reservas confirmadas permanecem.
### Validação
Histórico temporal e política vigente.
### Requisitos relacionados
REQ-F-006, REQ-F-012, REQ-F-017.

## RULE-013 — Avaliações e tags
### Estado
Proposto.
### Regra
Após cada devolução, leitor responsável pode enviar avaliação opcional não editável de 1 a 5 para título e exemplar e sugerir tags rastreáveis.
### Exceções
Campos podem ser omitidos.
### Validação
Vínculo ao empréstimo devolvido e constraints de faixa.
### Requisitos relacionados
REQ-F-015.

## RULE-014 — Estados e intervenção administrativa
### Estado
Proposto.
### Regra
Administrador pode intervir em operações e transitar exemplares entre todos os estados definidos, preservando consistência e auditoria.
### Exceções
Transição conflitante é recusada.
### Validação
Autorização, invariantes e trilha.
### Requisitos relacionados
REQ-F-016, REQ-F-018, REQ-F-019.

## RULE-015 — Configuração com vigência
### Estado
Proposto.
### Regra
Mudança de política é auditada e não altera silenciosamente reservas confirmadas; suspensão global bloqueia apenas novas reservas.
### Exceções
Intervenção administrativa explícita e auditada.
### Validação
Versionamento ou snapshot da política aplicável.
### Requisitos relacionados
REQ-F-017 a REQ-F-019.
