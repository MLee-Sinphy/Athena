# PROJECT_CONTEXT.md

> Este arquivo recebe o contexto humano inicial do Athena.
> As instruções entre colchetes são gabaritos, não dados do projeto.
> Preserve a ordem e use `Pendente` quando uma resposta ainda não existir.

## Identidade

### Nome
Athena.

### Descrição curta
Sistema online de aluguel de livros, composto por frontend web, backend com autenticação e módulos do domínio, além de persistência em banco de dados relacional.

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
[Problema.]

### Contexto
[Onde e quando ocorre.]

### Quem é afetado
- [Pessoa ou grupo.]

### Impacto
- [Consequência.]

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
Desenvolver, como projeto de estudo, um sistema online de aluguel de livros que funcione de ponta a ponta enquanto seu backend estiver em execução.

### Objetivos secundários
- [Objetivo.]

### Não objetivos
- Manter o sistema disponível 24 horas por dia.
- Tratar a primeira versão como um serviço comercial em produção.

### Critérios gerais de sucesso
- [Evidência verificável.]

## Público

### Público principal
[Usuário principal.]

### Públicos secundários
- [Público.]

### Necessidades do público
- [Necessidade.]

### Contexto de uso
[Ambiente, dispositivo e frequência.]

### Conhecimento esperado
[Conhecimento prévio.]

### Limitações e necessidades de acessibilidade
- [Necessidade.]

## Proposta

### Solução imaginada
[Solução em linguagem de produto.]

### Valor entregue
[Benefício concreto.]

### Diferenciais
- [Diferencial.]

### Hipótese de valor
[Hipótese.]

## Escopo

### Primeira versão
- Frontend web em React.
- Backend com autenticação e gerenciamento de usuários.
- Gerenciamento de livros.
- Gerenciamento de empréstimos de livros.
- Gerenciamento de reservas.
- Persistência em banco de dados relacional.
- Apresentação de mensagem de erro quando o frontend não conseguir acessar o backend.

### Fora da primeira versão
- [Capacidade adiada.]

### Fora do projeto
- [Item excluído.]

### Funcionalidades futuras conhecidas
- [Possibilidade futura.]

### Limites entre o sistema e o ambiente externo
- [Responsabilidade externa.]

## Comportamentos e regras

### Fluxo principal esperado
1. [Ação.]
2. [Resposta.]
3. [Resultado.]

### Fluxos alternativos conhecidos
1. [Condição e comportamento.]

### Exceções e falhas conhecidas
- Quando o backend estiver parado ou inacessível, o frontend deve informar ao usuário que não conseguiu acessar o serviço e não deve indicar que a operação foi concluída.

### Regras de negócio conhecidas
- [Regra.]

### Invariantes
- [Condição que nunca pode ser violada.]

### Dados de entrada
- [Dado.]

### Resultados e saídas
- [Dado ou efeito.]

## Experiência e interface

### Experiência desejada
- [Qualidade.]

### Experiência que deve ser evitada
- [Atrito.]

### Jornada principal do usuário
1. [Etapa.]

### Informações que precisam estar visíveis
- [Informação.]

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
- [Dado e tratamento.]

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
Usuários, livros, empréstimos e reservas devem persistir em banco de dados relacional. Política de retenção: Pendente.

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
- A primeira versão contemplará autenticação, usuários, livros, empréstimos e reservas.
- A indisponibilidade do backend deve ser informada claramente pelo frontend.

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
- Os livros alugados representam exemplares físicos, arquivos digitais ou ambos?
- O sistema será apenas uma biblioteca demonstrativa ou haverá alguma simulação de pagamento pelo aluguel?

### Dúvidas de produto
- Quais tipos de usuário existirão e quais permissões cada um terá?
- Qual é a diferença pretendida entre reservar e realizar um empréstimo?
- Quais prazos, limites, renovações, atrasos, multas ou filas de espera existirão?
- O catálogo controlará apenas títulos ou também exemplares individuais de cada livro?

### Dúvidas técnicas
- Qual tecnologia será utilizada no backend?
- Qual sistema gerenciador de banco relacional será utilizado?
- A autenticação usará cookies de sessão ou tokens enviados pelo cliente?
- Será utilizado um domínio próprio ou o domínio padrão do GitHub Pages?

## Observações adicionais
[Contexto adicional.]
