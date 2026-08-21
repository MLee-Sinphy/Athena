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
Leitores e administradores utilizam uma aplicação web vinculada ao acervo físico da instituição, tanto em computadores quanto em dispositivos móveis.

### Conhecimento esperado
[Conhecimento prévio.]

### Limitações e necessidades de acessibilidade
- A interface deve permanecer compreensível, operável e visualmente consistente em computadores e dispositivos móveis.

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
- Login por um único campo que aceita e-mail ou matrícula/identificador, acompanhado da senha.
- Primeiro acesso com troca obrigatória da senha temporária criada pelo administrador.
- Recuperação inicial de acesso assistida pelo administrador, sem envio de e-mail na primeira versão.
- Gerenciamento de livros.
- Pesquisa textual por título, autor, ISBN, categoria, descrição e palavras-chave, acompanhada de filtros do catálogo.
- Gerenciamento de empréstimos de livros.
- Gerenciamento de reservas.
- Calendário de reserva e empréstimo baseado nos dias em que a biblioteca funciona.
- Cadastro administrativo de feriados e fechamentos excepcionais.
- Painel administrativo para configurar intervalos mínimo e máximo, limite de empréstimos, permissões e efeitos de penalidades.
- Configuração administrativa dos dias regulares de funcionamento, com segunda a sexta-feira como padrão inicial brasileiro.
- Fila de espera ordenada para títulos sem exemplar disponível no período desejado.
- Cadastro de leitores pelo administrador e alteração do próprio e-mail e senha pelo leitor.
- Visibilidade, alteração e cancelamento de qualquer empréstimo pelo administrador.
- Alteração e cancelamento da própria reserva pelo leitor, desde que a mudança não conflite com reserva já confirmada de outra pessoa.
- Prorrogação da devolução após a retirada, condicionada à ausência de fila e ao período máximo configurado.
- Controle configurável de cancelamentos frequentes e suas penalidades.
- Tolerância configurável para retirada, com padrão inicial de 1 dia de funcionamento.
- Reorganização da disponibilidade quando uma reserva expirar sem retirada.
- Log persistente de auditoria das ações administrativas sobre empréstimos e configurações.
- Avaliação opcional do título e do estado físico do exemplar pelo leitor ao concluir a devolução.
- Persistência em banco de dados relacional.
- Apresentação de mensagem de erro quando o frontend não conseguir acessar o backend.

### Fora da primeira versão
- Notificação por e-mail quando uma devolução antecipada permitir que o próximo leitor retire o exemplar antes da data reservada.
- Central de notificações internas para eventos de antecipação e perda de prioridade.
- Recuperação autônoma de senha por e-mail.

### Fora do projeto
- Cobrança por empréstimo ou processamento de pagamentos.
- Distribuição de livros ou arquivos digitais.

### Funcionalidades futuras conhecidas
- Notificações internas e por e-mail vinculadas à fila de espera, à perda de prioridade e às devoluções antes do prazo.
- Recuperação autônoma de senha por e-mail.

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
7. Antes da retirada, o leitor pode alterar as datas de retirada e devolução, desde que o novo período não conflite com outra reserva confirmada.
8. Depois da retirada, o leitor pode alterar somente a data de devolução, desde que não haja outra pessoa na fila e o período resultante não ultrapasse o máximo configurado.
9. Quando o leitor cancelar reservas acima do limite configurado dentro da janela aplicável, novas solicitações podem ser bloqueadas sem cancelar as reservas já confirmadas.

### Exceções e falhas conhecidas
- Quando o backend estiver parado ou inacessível, o frontend deve informar ao usuário que não conseguiu acessar o serviço e não deve indicar que a operação foi concluída.

### Regras de negócio conhecidas
- Somente leitores cadastrados por um administrador podem solicitar empréstimos.
- O administrador cadastra o leitor com matrícula ou identificador institucional, e-mail e senha inicial.
- A senha inicial é temporária e deve ser substituída obrigatoriamente no primeiro acesso.
- O sistema pode sugerir uma senha inicial aleatória gerada de forma criptograficamente segura.
- A matrícula ou o identificador institucional deve ser único dentro de cada instituição.
- O e-mail do leitor deve ser único dentro de cada instituição.
- O leitor pode alterar o próprio e-mail e a própria senha depois de cadastrado.
- O formulário de login possui um único identificador, que aceita o e-mail ou a matrícula/identificador institucional, e um campo separado para a senha.
- Enquanto o envio de e-mail não fizer parte do sistema, a recuperação de acesso é realizada com assistência do administrador e resulta em nova senha temporária.
- Não há cobrança financeira pelo empréstimo; o direito básico decorre do cadastro do leitor na instituição.
- Todo exemplar físico deve possuir identificação única no sistema.
- Vários exemplares do mesmo livro devem aparecer agrupados como um único título no catálogo do leitor.
- Um empréstimo concedido deve estar associado a um exemplar físico específico.
- O leitor deve solicitar uma reserva mesmo quando houver disponibilidade imediata.
- O leitor escolhe o intervalo do empréstimo dentro do mínimo e do máximo configurados pelo administrador.
- Os valores padrão do intervalo são no mínimo 3 e no máximo 15 dias de funcionamento da biblioteca.
- Somente dias de funcionamento configurados para a biblioteca contam para determinar os intervalos permitidos.
- O administrador pode cadastrar feriados e fechamentos excepcionais, que não contam como dias de funcionamento.
- Por padrão, os dias regulares de funcionamento são de segunda a sexta-feira; o administrador pode alterar livremente os dias em que sua biblioteca funciona.
- As datas de retirada e devolução devem ser definidas e respeitadas.
- Quando não houver disponibilidade imediata, o leitor pode escolher um período futuro e participar de uma fila de espera ordenada.
- A fila de espera deve respeitar a ordem cronológica das solicitações: quem solicita primeiro possui prioridade para reservar o período disponível.
- O atraso pode gerar uma penalidade configurável, incluindo suspensão temporária e redução do limite de empréstimos simultâneos.
- A configuração padrão para atraso suspende novos empréstimos e novas reservas por 7 dias corridos; o administrador pode alterar essa política no painel.
- Um leitor com empréstimo atrasado não pode criar novas reservas enquanto o atraso persistir ou durante a penalidade aplicável.
- A quantidade máxima de empréstimos simultâneos é configurada pelo administrador e pode ser modificada pelas penalidades aplicáveis ao leitor.
- A quantidade máxima padrão é de 3 empréstimos simultâneos.
- A tolerância para retirada é configurada pelo administrador e possui valor padrão de 1 dia de funcionamento da biblioteca.
- Se o leitor não retirar o exemplar dentro da tolerância, ele perde a prioridade daquela reserva.
- O próximo leitor da fila deve ser notificado e pode aceitar ou recusar a antecipação da retirada até a data em que sua reserva original começaria.
- Se recusar a antecipação, o leitor preserva integralmente sua reserva original.
- Se o próximo leitor não aceitar a antecipação, outro leitor pode usar o período livre, desde que nenhuma reserva confirmada seja afetada.
- O leitor pode cancelar a própria reserva em qualquer momento anterior à retirada.
- Antes da retirada, o leitor pode alterar as datas de retirada e devolução sem sobrepor qualquer período já confirmado para outro leitor.
- Depois da retirada, uma renovação corresponde à alteração da data de devolução e só é permitida quando não houver outra pessoa na fila e o período resultante não ultrapassar o máximo configurado.
- Cancelamentos realizados pelo leitor são contados em uma janela móvel de 1 mês iniciada no primeiro cancelamento relevante; a contagem reinicia ao fim dessa janela.
- Para a regra padrão, 1 mês corresponde a uma janela exata de 30 dias contados a partir do primeiro cancelamento relevante.
- O limite padrão é de 3 cancelamentos do leitor dentro da janela; ao ultrapassá-lo, novas solicitações ficam bloqueadas até o fim da mesma janela.
- Cancelamentos realizados pelo administrador não entram na contagem do leitor.
- A penalidade por cancelamentos frequentes bloqueia somente novas solicitações e preserva reservas já confirmadas.
- A concessão não exige confirmação do administrador quando todas as regras forem satisfeitas.
- O administrador pode visualizar, alterar e cancelar qualquer empréstimo.
- Alterações e cancelamentos administrativos devem gerar registro persistente de auditoria para consulta futura.
- Cada registro de auditoria deve guardar autor, data e hora, ação, valor anterior e valor novo; a justificativa é opcional.
- O administrador pode suspender novas reservas sem cancelar ou alterar reservas já confirmadas.
- O administrador pode restaurar para disponível um exemplar danificado, em manutenção, perdido ou descartado, e a transição deve ser auditada.
- Nenhuma transição de estado do exemplar exige confirmação adicional além da ação autenticada do administrador.
- O painel administrativo deve permitir configurar: dias regulares de funcionamento; feriados e fechamentos; prazo mínimo e máximo; limite simultâneo; tolerância para retirada; punição por atraso; limite e punição por cancelamentos; permissão para renovação; e suspensão global de novas reservas.
- Ao finalizar a devolução, o leitor pode avaliar separadamente o conteúdo do título e o estado físico do exemplar devolvido.
- As médias devem ser derivadas das avaliações individuais: a avaliação do título compõe a média do título, enquanto a avaliação física compõe a média do exemplar específico.
- As duas avaliações usam escala de 0 a 5 estrelas.
- Cada devolução concluída permite uma nova avaliação independente do título e do exemplar pelo leitor responsável pelo empréstimo.
- Uma avaliação enviada não pode ser editada pelo leitor.
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
- Um empréstimo retirado não pode ter sua data de início modificada pelo leitor.
- A prorrogação de um empréstimo retirado não pode prejudicar uma pessoa já presente na fila.
- A visualização da fila pelo leitor não pode revelar nome, matrícula, e-mail ou qualquer outro dado que identifique as demais pessoas.

### Dados de entrada
- Cadastro do leitor, incluindo matrícula ou identificador institucional, e-mail e senha inicial.
- Dados obrigatórios do título: título, autor, ISBN, editora, edição, ano, categoria, descrição e imagem principal de capa.
- Dados opcionais do título: número de páginas e imagens adicionais.
- Código único e dados operacionais de cada exemplar físico.
- Solicitação de empréstimo ou reserva.
- Configurações administrativas de tolerância, penalidade, limite e demais políticas.
- Dias regulares de funcionamento, feriados e fechamentos excepcionais.
- Alteração ou cancelamento de reserva pelo leitor.
- Alteração ou cancelamento de empréstimo pelo administrador, com dados necessários para auditoria.
- Avaliações individuais do título e do estado físico do exemplar, vinculadas ao leitor e à devolução concluída.

### Resultados e saídas
- Catálogo de títulos e sua disponibilidade para o leitor.
- Resultados de pesquisa textual e filtros por título, autor, ISBN, categoria, descrição, palavras-chave, disponibilidade, avaliação e ano.
- Decisão de aprovação ou recusa da solicitação conforme as regras configuradas.
- Associação entre leitor, período reservado, empréstimo e exemplar físico específico.
- Visão administrativa do estado de cada exemplar.
- Nova disponibilidade decorrente da expiração de uma reserva não retirada.
- Notificação ao próximo leitor elegível e registro de sua resposta.
- Histórico consultável das alterações administrativas.
- Registro de envio, leitura, aceite e recusa das notificações.
- Estado operacional do exemplar: disponível, reservado, emprestado, danificado, em manutenção, perdido ou descartado.
- Média das avaliações do título e média das avaliações do estado físico de cada exemplar.

## Experiência e interface

### Experiência desejada
- Moderna, minimalista e visualmente bela.
- Clara, responsiva e eficiente, sem elementos decorativos que prejudiquem o uso.
- Consistente entre computadores e dispositivos móveis.

### Experiência que deve ser evitada
- Interface visualmente carregada, com excesso de animações, adornos ou informações sem hierarquia.
- Experiência incompleta ou difícil de usar em telas móveis.
- Exposição de identidade ou dados de outros leitores em filas, reservas ou empréstimos.

### Jornada principal do usuário
1. O leitor autentica-se pelo campo de e-mail ou matrícula e senha.
2. Pesquisa ou filtra o catálogo por título, autor, ISBN, categoria, descrição, palavra-chave, disponibilidade, avaliação ou ano.
3. Abre os detalhes de um título, consulta descrição, avaliação, disponibilidade e calendário.
4. Escolhe um período válido e solicita a reserva.
5. Acompanha confirmação, posição na fila, datas estimadas, empréstimos, devoluções e eventuais penalidades sem visualizar dados de outros leitores.
6. Depois da devolução, pode avaliar o título e o estado físico do exemplar.

### Informações que precisam estar visíveis
- Para o leitor: dados bibliográficos, disponibilidade agregada, calendário, datas confirmadas e média de avaliação do título, sem necessidade de exibir o código único de cada exemplar.
- Para o leitor: sua posição na fila e datas estimadas, sem nome, matrícula, e-mail ou qualquer identificador das demais pessoas.
- Para o administrador: título, exemplares individuais, códigos únicos, estado e empréstimo associado.
- Para o administrador: avaliações e média do estado físico de cada exemplar.
- Para o administrador: painel das políticas vigentes e controles para alterar ou cancelar empréstimos.

### Estados importantes da interface
- Carregamento.
- Vazio.
- Erro.
- Sucesso.
- Backend indisponível.

### Dispositivos e tamanhos de tela
- Computadores desktop e notebooks.
- Smartphones.
- A experiência responsiva é requisito fundamental; nenhuma função essencial pode existir apenas em um dos contextos.

### Acessibilidade
- [Expectativa.]

## Restrições

### Técnicas
- O frontend deve utilizar React e ser publicável no GitHub Pages.
- O frontend utilizará o endereço padrão do GitHub Pages, sem domínio próprio na primeira versão.
- O frontend deve consumir o backend por HTTPS.
- O backend deve poder ser hospedado em um VPS da Hostinger; planos Web e Cloud comuns não atendem ao runtime Python/Django escolhido.
- A persistência deve utilizar banco de dados relacional.

### Tecnologias proibidas
- [Tecnologia e motivo.]

### Segurança
- O backend deve possuir autenticação e autorização apropriadas aos tipos de usuário.
- Segredos e credenciais do banco não podem ser expostos no frontend.
- Senhas escolhidas pelo usuário devem possuir no mínimo 15 caracteres e o sistema deve aceitar pelo menos 64 caracteres, incluindo espaços e caracteres Unicode normalizados.
- O sistema não deve impor combinações obrigatórias de maiúsculas, minúsculas, números e símbolos; deve bloquear senhas comuns ou conhecidas como comprometidas e oferecer medidor de força.
- O gerador de senha deve usar fonte criptograficamente segura e pode combinar letras, números e símbolos.
- Senhas devem ser armazenadas somente por meio do mecanismo de hash seguro do framework, nunca em texto puro ou de forma reversível.
- Tentativas de autenticação devem possuir limitação de frequência.
- Sessões expiram após 30 minutos de inatividade e possuem duração absoluta máxima de 8 horas, com invalidação aplicada pelo backend.
- Logout, expiração, troca e recuperação de senha devem invalidar as sessões ou credenciais aplicáveis.
- Depois do login, o backend emite um token bearer opaco, aleatório, de curta duração e revogável; o frontend o envia no cabeçalho `Authorization` das requisições autenticadas.
- O token deve permanecer somente na memória do frontend e não pode ser persistido em `localStorage`, `sessionStorage` ou armazenamento equivalente.
- O backend deve armazenar somente uma representação segura do token, nunca seu valor reutilizável em texto puro.
- Atualizar, fechar ou reabrir o frontend pode exigir novo login, pois não haverá credencial persistente no navegador.
- CORS deve permitir somente a origem exata do frontend publicado no GitHub Pages e os métodos e cabeçalhos necessários.

### Privacidade e dados sensíveis
- Dados cadastrais e histórico de empréstimos dos leitores devem ser acessíveis somente de acordo com as permissões definidas.
- Posições e estimativas da fila devem ser apresentadas sem revelar a identidade ou os dados pessoais dos outros leitores.

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
- Backend Python com Django e Django REST Framework: API, autenticação, autorização, usuários, livros, empréstimos, reservas e regras de negócio.
- PostgreSQL acessado pelo Django ORM: persistência relacional e migrações.
- Armazenamento de objetos ou serviço de mídia: arquivos de imagem; o banco mantém referências e metadados.

### Fluxo de dados esperado
1. O usuário informa e-mail ou matrícula/identificador e senha no frontend.
2. O frontend envia as credenciais ao backend exclusivamente por HTTPS.
3. O backend valida o login e devolve um token bearer opaco e revogável.
4. O frontend mantém o token somente em memória e o envia no cabeçalho `Authorization` das requisições autenticadas.
5. O backend valida o token, autentica e autoriza a operação, aplica regras de negócio e acessa o banco quando necessário.
6. O backend devolve uma resposta ao frontend.
7. O frontend apresenta o resultado ou uma mensagem de indisponibilidade quando não conseguir acessar o backend.

### Persistência
Usuários, títulos, exemplares físicos e seus estados, calendários de funcionamento, feriados, fechamentos excepcionais, políticas configuráveis, penalidades, empréstimos, reservas, posições da fila de espera, avaliações individuais, notificações e registros de auditoria devem persistir em banco de dados relacional. Um título pode possuir vários exemplares, e cada exemplar deve possuir identificação única. As avaliações individuais são a fonte de verdade; suas médias podem ser calculadas sob demanda ou mantidas como dados derivados, sem substituir o histórico. Política de retenção: Pendente.

### Integrações externas
- Armazenamento de imagens: serviço ou mecanismo ainda pendente; preferencialmente os arquivos ficam fora do banco relacional e o banco armazena metadados e URLs.

### Tecnologias desejadas
- React para o frontend, como tecnologia de estudo definida pelo responsável.
- Python com Django e Django REST Framework para o backend, aproveitando a familiaridade do responsável e os recursos maduros de autenticação, administração, ORM, migrações e APIs.
- PostgreSQL como sistema gerenciador de banco de dados relacional.
- Django ORM para modelagem, consultas e migrações.
- Armazenamento de objetos compatível com a infraestrutura escolhida para imagens; PostgreSQL armazena URLs, metadados e relações, não os arquivos binários por padrão.

### Ambientes e deploy
- Frontend publicável no GitHub Pages.
- Backend publicável em VPS da Hostinger e executado sob demanda; não há requisito de operação contínua.
- O VPS deve executar Python/Django, PostgreSQL e os serviços necessários à API com HTTPS; a topologia operacional definitiva será formalizada em `ARCHITECTURE.md`.

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
- O backend deverá ser hospedável em VPS da Hostinger e poderá ser executado sob demanda.
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
- O administrador pode cadastrar feriados e fechamentos excepcionais.
- O intervalo padrão de empréstimo é de 3 a 15 dias de funcionamento, configurável pelo administrador.
- O limite padrão é de 3 empréstimos simultâneos, configurável pelo administrador.
- A penalidade padrão por atraso bloqueia novos empréstimos e reservas por 7 dias corridos.
- Leitores com empréstimos atrasados não podem criar novas reservas.
- Renovação é a alteração da devolução e exige ausência de fila e respeito ao período máximo.
- O leitor pode cancelar antes da retirada; mais de 3 cancelamentos em uma janela móvel de 1 mês bloqueiam novas solicitações até o fim da janela.
- Cancelamentos administrativos não contam para a punição, e reservas já confirmadas são preservadas.
- O administrador pode suspender novas reservas sem afetar as existentes.
- Notificações futuras registrarão envio, leitura, aceite e recusa.
- A auditoria registra autor, data e hora, ação, valor anterior e novo; justificativa é opcional.
- Exemplares podem transitar entre disponível, reservado, emprestado, danificado, em manutenção, perdido e descartado, inclusive retornar de qualquer desses estados por ação administrativa.
- Os dias de funcionamento padrão são segunda a sexta-feira, mas podem ser alterados pelo administrador.
- Matrícula ou identificador e e-mail são únicos dentro de cada instituição.
- Título, autor, ISBN, editora, edição, ano, categoria, descrição e imagem principal de capa são obrigatórios; número de páginas e imagens adicionais são opcionais.
- O leitor pode avaliar o título e o estado físico do exemplar após concluir a devolução; as médias são derivadas das avaliações individuais.
- A escala de avaliação é de 0 a 5 estrelas; cada devolução pode gerar uma avaliação independente e avaliações enviadas não podem ser editadas.
- O backend será desenvolvido em Python com Django e Django REST Framework, usando PostgreSQL e Django ORM.
- O login usa um único campo para e-mail ou matrícula/identificador e um campo de senha.
- A senha inicial é temporária e deve ser alterada no primeiro acesso.
- Na primeira versão, recuperação de acesso é assistida pelo administrador; recuperação autônoma por e-mail fica para o futuro.
- A política de senha prioriza comprimento mínimo de 15 caracteres, bloqueio de senhas comuns/comprometidas, suporte a gerador seguro e ausência de regras obrigatórias de composição.
- A sessão expira após 30 minutos de inatividade ou 8 horas de duração absoluta.
- Imagens ficam preferencialmente em armazenamento de objetos, com referências e metadados no PostgreSQL.
- O frontend usará o endereço padrão do GitHub Pages na primeira versão.
- A autenticação entre os domínios usará token bearer opaco e revogável, mantido somente na memória do React e enviado no cabeçalho `Authorization`.
- Tokens não serão persistidos no armazenamento do navegador; recarregar ou reabrir a aplicação pode exigir novo login.
- CORS aceitará somente a origem exata do frontend publicado.
- O frontend será responsivo e funcional em computadores e smartphones, com apresentação moderna e minimalista.
- A fila exibirá posição e estimativas sem identificar outros leitores.

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
- Nenhuma identificada neste bloco no momento.

### Dúvidas técnicas
- Qual provedor de armazenamento de objetos será compatível com a hospedagem e o orçamento escolhidos?

## Observações adicionais
[Contexto adicional.]
