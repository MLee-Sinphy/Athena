# PROJECT_CONTEXT.md

> Este arquivo recebe o contexto humano inicial do Athena.
> As instruções entre colchetes são gabaritos, não dados do projeto.
> Preserve a ordem e use `Pendente` quando uma resposta ainda não existir.

## Identidade

### Nome
Athena.

### Descrição curta
Sistema online de empréstimo de livros físicos para escolas, universidades, bibliotecas públicas e instituições semelhantes, composto por frontend web, backend com autenticação e módulos do domínio, além de persistência em banco de dados relacional.

### Estado atual
Planejamento.

### Responsável
Lee.

## Origem e motivação

### Como a ideia surgiu
O projeto surgiu como objeto de estudo prático de desenvolvimento de um sistema web completo com frontend, backend, autenticação, banco relacional, documentação e deploy distribuído.

### Por que vale a pena resolver
Permitir o estudo integrado de engenharia de software, incluindo regras de negócio, arquitetura cliente-servidor, APIs, autenticação, persistência, testes, documentação e operação.

### Resultado que motivou o projeto
Construir e compreender um sistema completo a partir de documentação validada, usando desenvolvimento incremental assistido por IA.

## Problema

### Descrição
Leitores precisam consultar um acervo físico, reservar períodos de uso e solicitar empréstimos, enquanto a instituição precisa configurar suas políticas, controlar a disponibilidade e identificar exatamente qual exemplar foi entregue a cada pessoa.

### Contexto
O problema ocorre em escolas, universidades, bibliotecas públicas e instituições semelhantes que mantêm acervos de exemplares físicos administrados por pessoas responsáveis pela biblioteca.

### Quem é afetado
- Leitores cadastrados, como alunos, universitários, clientes ou usuários de bibliotecas públicas.
- Administradores responsáveis pelos cadastros, pelo acervo, pelas políticas, pelas reservas e pelos empréstimos.

### Impacto
- O leitor precisa saber quais títulos estão disponíveis, reservar um período e organizar previamente as datas de retirada e devolução.
- A instituição precisa aplicar regras configuráveis de elegibilidade e manter rastreabilidade sobre cada exemplar físico.

### Frequência e dimensão
[Frequência e escala.]

### Causas conhecidas ou suspeitas
- [Causa ou hipótese.]

### Como o problema é resolvido atualmente
[Solução atual.]

### Limitações das soluções atuais
- [Limitação.]

### Aspectos atuais que devem ser preservados
- [Aspecto.]

## Objetivos

### Objetivo principal
Desenvolver, como projeto de estudo, um sistema configurável de empréstimo de livros físicos que possa atender diferentes tipos de biblioteca e funcione de ponta a ponta enquanto seu backend estiver em execução.

### Objetivos secundários
- [Objetivo.]

### Não objetivos
- Manter o sistema disponível 24 horas por dia.
- Tratar a primeira versão como um serviço comercial em produção.

### Critérios gerais de sucesso
- [Evidência verificável.]

## Público

### Público principal
Leitores cadastrados pela instituição, incluindo alunos, universitários, clientes e usuários de bibliotecas públicas.

### Públicos secundários
- Administradores da plataforma responsáveis pelos usuários, pelo acervo e pelas políticas da biblioteca.

### Necessidades do público
- Leitores precisam consultar o catálogo, escolher períodos válidos, reservar e solicitar empréstimos sem precisar distinguir cópias equivalentes de um mesmo título.
- Administradores precisam cadastrar títulos e exemplares físicos, identificar cada cópia e acompanhar empréstimos e ocorrências.
- Administradores precisam configurar as regras que determinam prazos, limites, permissões, penalidades e demais condições de empréstimo.

### Contexto de uso
Leitores e administradores utilizam uma aplicação web vinculada ao acervo físico da instituição.

### Conhecimento esperado
[Conhecimento prévio.]

### Limitações e necessidades de acessibilidade
- [Necessidade.]

## Proposta

### Solução imaginada
Uma plataforma web configurável na qual administradores cadastram usuários e o acervo físico, definem políticas da biblioteca e acompanham as operações; leitores consultam títulos, escolhem datas válidas, fazem reservas e solicitam empréstimos sujeitos às regras da instituição.

### Valor entregue
Facilitar o acesso dos leitores ao acervo e permitir que diferentes instituições controlem disponibilidade, reservas, empréstimos e a situação individual de cada exemplar físico segundo suas próprias políticas.

### Diferenciais
- Catálogo simplificado para o leitor, agrupado por título.
- Controle individual de exemplares para o administrador sem expor detalhes operacionais desnecessários ao leitor.
- Painel administrativo para adaptar as políticas de empréstimo à dinâmica de cada biblioteca.

### Hipótese de valor
[Hipótese.]

## Escopo

### Primeira versão
- Frontend web em React.
- Backend com autenticação e gerenciamento de usuários.
- Gerenciamento de livros.
- Gerenciamento de empréstimos de livros.
- Gerenciamento de reservas.
- Calendário de reserva e empréstimo baseado nos dias em que a biblioteca funciona.
- Painel administrativo para configurar intervalos mínimo e máximo, limite de empréstimos, permissões e efeitos de penalidades.
- Fila de espera ordenada para títulos sem exemplar disponível no período desejado.
- Cadastro de leitores pelo administrador e alteração do próprio e-mail e senha pelo leitor.
- Visibilidade, alteração e cancelamento de qualquer empréstimo pelo administrador.
- Alteração e cancelamento da própria reserva pelo leitor, desde que a mudança não conflite com reserva já confirmada de outra pessoa.
- Tolerância configurável para retirada, com padrão inicial de 1 dia de funcionamento.
- Reorganização da disponibilidade quando uma reserva expirar sem retirada.
- Log persistente de auditoria das ações administrativas sobre empréstimos e configurações.
- Persistência em banco de dados relacional.
- Apresentação de mensagem de erro quando o frontend não conseguir acessar o backend.

### Fora da primeira versão
- Notificação por e-mail quando uma devolução antecipada permitir que o próximo leitor retire o exemplar antes da data reservada.

### Fora do projeto
- Cobrança por empréstimo ou processamento de pagamentos.
- Distribuição de livros ou arquivos digitais.

### Funcionalidades futuras conhecidas
- Notificação antecipada por e-mail vinculada à fila de espera e às devoluções antes do prazo.

### Limites entre o sistema e o ambiente externo
- O sistema controla registros e solicitações, mas a entrega e a devolução do exemplar físico ocorrem na instituição responsável pelo acervo.
- A relação institucional do leitor e qualquer cobrança externa existem fora do Athena; estar cadastrado pelo administrador representa o direito básico de solicitar empréstimos, sujeito às demais regras configuradas.

## Comportamentos e regras

### Fluxo principal esperado
1. Um administrador cadastra um título e seus exemplares físicos, atribuindo identificação única a cada exemplar.
2. Um leitor cadastrado pelo administrador autentica-se e consulta o catálogo, no qual cópias do mesmo livro aparecem agrupadas pelo título.
3. O leitor escolhe, em um calendário, datas de retirada e devolução permitidas pelas políticas configuradas e pelos dias de funcionamento da biblioteca.
4. O leitor solicita a reserva do título para o período escolhido.
5. O sistema avalia as regras aplicáveis ao leitor, ao título, ao período e aos exemplares disponíveis.
6. Quando houver exemplar disponível e as regras permitirem, a reserva e o empréstimo são concedidos sem exigir confirmação administrativa.
7. Um exemplar específico é associado ao empréstimo e o administrador pode acompanhar, alterar ou cancelar a operação.

### Fluxos alternativos conhecidos
1. Quando nenhuma cópia estiver disponível imediatamente, o leitor pode reservar um período futuro e entra em uma fila de espera organizada.
2. Quando uma devolução antecipada liberar o exemplar, o próximo leitor pode retirá-lo antes da data reservada e manter a data final originalmente definida, mesmo que o período total ultrapasse excepcionalmente o máximo normal.
3. Quando o leitor não satisfizer uma regra configurada de empréstimo, a solicitação deve ser recusada com uma explicação apropriada.
4. Quando um empréstimo for devolvido depois da data, a penalidade configurada pode impedir novos empréstimos por um período e reduzir o limite de livros permitido.
5. Quando o leitor não retirar o exemplar dentro da tolerância configurada, sua reserva perde a prioridade; o próximo leitor da fila deve ser avisado e consultado sobre o interesse em antecipar sua retirada.
6. Quando o próximo leitor não aceitar a antecipação, o exemplar pode ser disponibilizado para outro leitor no período livre, sem afetar reservas futuras confirmadas.

### Exceções e falhas conhecidas
- Quando o backend estiver parado ou inacessível, o frontend deve informar ao usuário que não conseguiu acessar o serviço e não deve indicar que a operação foi concluída.

### Regras de negócio conhecidas
- Somente leitores cadastrados por um administrador podem solicitar empréstimos.
- O administrador cadastra o leitor com matrícula ou identificador institucional, e-mail e senha inicial.
- O leitor pode alterar o próprio e-mail e a própria senha depois de cadastrado.
- Não há cobrança financeira pelo empréstimo; o direito básico decorre do cadastro do leitor na instituição.
- Todo exemplar físico deve possuir identificação única no sistema.
- Vários exemplares do mesmo livro devem aparecer agrupados como um único título no catálogo do leitor.
- Um empréstimo concedido deve estar associado a um exemplar físico específico.
- O leitor deve solicitar uma reserva mesmo quando houver disponibilidade imediata.
- O leitor escolhe o intervalo do empréstimo dentro do mínimo e do máximo configurados pelo administrador.
- Somente dias de funcionamento configurados para a biblioteca contam para determinar os intervalos permitidos.
- As datas de retirada e devolução devem ser definidas e respeitadas.
- Quando não houver disponibilidade imediata, o leitor pode escolher um período futuro e participar de uma fila de espera ordenada.
- A fila de espera deve respeitar a ordem cronológica das solicitações: quem solicita primeiro possui prioridade para reservar o período disponível.
- O atraso pode gerar uma penalidade configurável, incluindo suspensão temporária e redução do limite de empréstimos simultâneos.
- A configuração padrão para atraso suspende novos empréstimos por 1 semana; o administrador pode alterar essa política no painel.
- A quantidade máxima de empréstimos simultâneos é configurada pelo administrador e pode ser modificada pelas penalidades aplicáveis ao leitor.
- A tolerância para retirada é configurada pelo administrador e possui valor padrão de 1 dia de funcionamento da biblioteca.
- Se o leitor não retirar o exemplar dentro da tolerância, ele perde a prioridade daquela reserva.
- O próximo leitor da fila deve ser notificado e pode aceitar ou recusar a antecipação da retirada; o canal e o prazo de resposta ainda precisam ser definidos.
- Se o próximo leitor não aceitar a antecipação, outro leitor pode usar o período livre, desde que nenhuma reserva confirmada seja afetada.
- O leitor pode alterar ou cancelar a própria reserva.
- Uma alteração feita pelo leitor não pode prolongar ou deslocar sua reserva de modo a sobrepor qualquer período já confirmado para outro leitor.
- A concessão não exige confirmação do administrador quando todas as regras forem satisfeitas.
- O administrador pode visualizar, alterar e cancelar qualquer empréstimo.
- Alterações e cancelamentos administrativos devem gerar registro persistente de auditoria para consulta futura.
- Uma devolução antecipada pode antecipar a retirada do próximo leitor sem antecipar obrigatoriamente sua data final, constituindo exceção permitida ao período máximo normal.

### Invariantes
- Um exemplar físico não pode estar associado simultaneamente a mais de um empréstimo ativo.
- Cada exemplar deve possuir um identificador único.
- O leitor não deve precisar escolher nem visualizar o código interno do exemplar para solicitar um título.
- O administrador deve conseguir identificar exatamente qual exemplar participa de cada empréstimo.
- Nenhum período confirmado pode sobrepor o uso do mesmo exemplar por leitores diferentes.
- Uma alteração de reserva não pode reduzir nem invalidar o período confirmado de outro leitor.
- A ordem de prioridade da fila não pode ser modificada sem uma nova decisão explícita de produto.
- Registros de auditoria não podem ser alterados ou apagados por operações administrativas comuns.

### Dados de entrada
- Cadastro do leitor, incluindo matrícula ou identificador institucional, e-mail e senha inicial.
- Dados bibliográficos do título.
- Código único e dados operacionais de cada exemplar físico.
- Solicitação de empréstimo ou reserva.
- Configurações administrativas de tolerância, penalidade, limite e demais políticas.
- Alteração ou cancelamento de reserva pelo leitor.
- Alteração ou cancelamento de empréstimo pelo administrador, com dados necessários para auditoria.

### Resultados e saídas
- Catálogo de títulos e sua disponibilidade para o leitor.
- Decisão de aprovação ou recusa da solicitação conforme as regras configuradas.
- Associação entre leitor, período reservado, empréstimo e exemplar físico específico.
- Visão administrativa do estado de cada exemplar.
- Nova disponibilidade decorrente da expiração de uma reserva não retirada.
- Notificação ao próximo leitor elegível e registro de sua resposta.
- Histórico consultável das alterações administrativas.

## Experiência e interface

### Experiência desejada
- [Qualidade.]

### Experiência que deve ser evitada
- [Atrito.]

### Jornada principal do usuário
1. [Etapa.]

### Informações que precisam estar visíveis
- Para o leitor: título, disponibilidade agregada, calendário e datas confirmadas, sem necessidade de exibir o código único de cada exemplar.
- Para o administrador: título, exemplares individuais, códigos únicos, estado e empréstimo associado.
- Para o administrador: painel das políticas vigentes e controles para alterar ou cancelar empréstimos.

### Estados importantes da interface
- Carregamento.
- Vazio.
- Erro.
- Sucesso.
- Backend indisponível.

### Dispositivos e tamanhos de tela
- [Dispositivo.]

### Acessibilidade
- [Expectativa.]

## Restrições

### Técnicas
- O frontend deve utilizar React e ser publicável no GitHub Pages.
- O frontend deve consumir o backend por HTTPS.
- O backend deve poder ser hospedado na Hostinger.
- A persistência deve utilizar banco de dados relacional.

### Tecnologias proibidas
- [Tecnologia e motivo.]

### Segurança
- O backend deve possuir autenticação e autorização apropriadas aos tipos de usuário.
- Segredos e credenciais do banco não podem ser expostos no frontend.

### Privacidade e dados sensíveis
- Dados cadastrais e histórico de empréstimos dos leitores devem ser acessíveis somente de acordo com as permissões definidas.

### Legais e regulatórias
- [Restrição.]

### Financeiras
- [Orçamento ou limite.]

### Prazo
- Não há exigência de disponibilidade contínua; o backend pode ser iniciado e interrompido conforme as sessões de estudo e demonstração.

### Desempenho e escala
- [Meta ou volume.]

### Compatibilidade
- [Sistema, navegador ou dispositivo.]

## Arquitetura imaginada

### Visão geral
Frontend React publicado no GitHub Pages, comunicando-se por HTTPS com um backend hospedável na Hostinger, que centraliza autenticação, regras de negócio e acesso ao banco relacional. Esta é uma arquitetura imaginada e ainda deverá ser formalmente avaliada e validada.

### Componentes principais
- Frontend React: interface do usuário e consumo da API.
- Backend: autenticação, usuários, livros, empréstimos, reservas e regras de negócio.
- Banco relacional: persistência dos dados do sistema.

### Fluxo de dados esperado
1. O usuário interage com o frontend.
2. O frontend envia uma requisição HTTPS ao backend.
3. O backend autentica e autoriza a operação, aplica regras de negócio e acessa o banco quando necessário.
4. O backend devolve uma resposta ao frontend.
5. O frontend apresenta o resultado ou uma mensagem de indisponibilidade quando não conseguir acessar o backend.

### Persistência
Usuários, títulos, exemplares físicos, calendários de funcionamento, políticas configuráveis, penalidades, empréstimos, reservas, posições da fila de espera, notificações e registros de auditoria devem persistir em banco de dados relacional. Um título pode possuir vários exemplares, e cada exemplar deve possuir identificação única. Política de retenção: Pendente.

### Integrações externas
- [Serviço e finalidade.]

### Tecnologias desejadas
- React para o frontend, como tecnologia de estudo definida pelo responsável.
- Banco de dados relacional para exercitar modelagem, relacionamentos e persistência transacional.
- Tecnologia do backend: Pendente.

### Ambientes e deploy
- Frontend publicável no GitHub Pages.
- Backend publicável na Hostinger e executado sob demanda; não há requisito de operação contínua.

## Desenvolvimento e qualidade

### Prioridades
1. Compreender e documentar o domínio e suas regras.
2. Construir o sistema incrementalmente a partir de testes e documentação validados.
3. Obter funcionamento ponta a ponta durante sessões de estudo e demonstração.

### Estratégia de testes esperada
- [Tipo de teste ou qualidade.]

### Critérios para considerar a primeira versão pronta
- [ ] [Critério verificável.]

### Manutenção esperada
Projeto mantido pelo responsável durante o período de estudo, sem compromisso de operação 24 horas por dia.

### Observabilidade esperada
- [Log, métrica ou alerta.]

## Riscos, hipóteses e dependências

### Riscos
- Backend desligado ou inacessível: operações dinâmicas ficam indisponíveis; o frontend deve comunicar claramente essa condição.
- Restrições do GitHub Pages para aplicações de página única: a estratégia de roteamento deverá ser definida antes da implementação.
- Restrições do plano da Hostinger para o runtime escolhido: validar antes de decidir a tecnologia do backend.

### Hipóteses que precisam ser validadas
- A hospedagem escolhida suportará o runtime, o processo e a conexão com o banco necessários ao backend.
- GitHub Pages e backend em outro domínio poderão comunicar-se de forma segura com a configuração escolhida de autenticação e CORS.

### Dependências externas
- [Dependência.]

### Decisões já tomadas
- O Athena é um objeto de estudo, não um serviço que precise permanecer disponível continuamente.
- O frontend será desenvolvido com React e deverá ser publicável no GitHub Pages.
- O frontend acessará o backend por HTTPS.
- O backend deverá ser hospedável na Hostinger e poderá ser executado sob demanda.
- A persistência usará banco de dados relacional.
- A primeira versão contemplará autenticação, usuários, livros, empréstimos, reservas, fila de espera, calendário e configuração administrativa de políticas.
- A indisponibilidade do backend deve ser informada claramente pelo frontend.
- O acervo será composto por exemplares físicos de livros.
- Não haverá cobrança ou pagamento pelo empréstimo.
- Existirão somente dois tipos de usuário: leitor e administrador; coordenadores e responsáveis pela biblioteca atuarão com perfil administrativo.
- O Athena não ficará limitado a escolas: poderá atender universidades, bibliotecas públicas e instituições semelhantes.
- O catálogo do leitor agrupará exemplares iguais por título.
- O controle administrativo e os empréstimos identificarão individualmente cada exemplar físico.
- Todo empréstimo começa por uma solicitação de reserva do leitor, inclusive quando houver disponibilidade imediata.
- O administrador configura o calendário de funcionamento e as políticas de empréstimo, incluindo períodos mínimo e máximo, limite simultâneo e efeitos de penalidades.
- A concessão permitida pelas regras não exige confirmação administrativa, mas o administrador pode visualizar, alterar e cancelar qualquer empréstimo.
- Leitores são cadastrados pelo administrador com matrícula ou identificador, e-mail e senha; depois podem alterar o próprio e-mail e senha.
- A notificação por e-mail em razão de devolução antecipada pertence a uma versão futura distante.
- A fila de espera usa a ordem cronológica da solicitação como prioridade.
- A tolerância para retirada é configurável, com padrão de 1 dia de funcionamento.
- A penalidade por atraso é configurável, com padrão de 1 semana sem novos empréstimos.
- O leitor pode alterar e cancelar reservas próprias, mas não pode criar conflito com período já reservado por outra pessoa.
- Operações administrativas relevantes devem produzir log persistente de auditoria.

## Referências

### Projetos semelhantes
- Referência:
- O que observar:
- O que não copiar:

### Referências visuais
- Referência:
- Elemento relevante:
- Intenção:

### Referências técnicas
- Referência:
- Por que é relevante:

### Artigos e documentos
- Referência:
- Informação importante:

## Questões em aberto

### Dúvidas estratégicas
- Nenhuma identificada até o momento.

### Dúvidas de produto
- Como tratar feriados e fechamentos excepcionais além dos dias semanais de funcionamento?
- Quais controles exatos estarão disponíveis na primeira versão do painel de políticas?
- Quais ações administrativas exigem justificativa obrigatória no log de auditoria?
- Quais ocorrências sobre um exemplar devem ser registradas, por exemplo dano, perda, manutenção ou descarte?
- Até qual momento o leitor pode alterar ou cancelar a própria reserva?
- Qual canal notificará o próximo leitor quando uma reserva expirar sem retirada?
- Quanto tempo o próximo leitor terá para aceitar a antecipação antes que o período seja oferecido a outra pessoa?
- Se o próximo leitor recusar a antecipação, ele preserva integralmente sua reserva futura original?

### Dúvidas técnicas
- Qual tecnologia será utilizada no backend?
- Qual sistema gerenciador de banco relacional será utilizado?
- A autenticação usará cookies de sessão ou tokens enviados pelo cliente?
- Será utilizado um domínio próprio ou o domínio padrão do GitHub Pages?

## Observações adicionais
[Contexto adicional.]
