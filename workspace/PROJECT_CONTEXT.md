# Contexto do projeto Athena

> Entrada humana para derivar a documentação oficial. Decisões não validadas permanecem explícitas como pendências.

## 1. Identidade e objetivo

- **Responsável:** M Lee. **Estado:** planejamento.
- Sistema web configurável para empréstimo gratuito de livros físicos em escolas, universidades, bibliotecas públicas e instituições semelhantes.
- Projeto de estudo full stack, documentado, testado e implantável; não é serviço comercial nem precisa operar 24 horas.
- Cada implantação atende uma instituição, com acervo, usuários, políticas e histórico isolados.
- Deve funcionar de ponta a ponta enquanto o backend estiver ativo e informar claramente quando estiver indisponível.

Leitores consultam o acervo, reservam períodos e acompanham empréstimos. Administradores controlam usuários, títulos, exemplares, calendário, políticas e ocorrências.

**Fora do projeto:** cobranças, pagamentos, aluguel comercial e distribuição de livros digitais.

## 2. Usuários e acesso

Existem somente dois perfis:

- **Leitor:** consulta o catálogo e gerencia as próprias operações dentro das regras.
- **Administrador:** cadastra leitores e acervo, configura políticas e pode acompanhar, alterar ou cancelar qualquer operação.

- O administrador cadastra o leitor com matrícula/identificador institucional, e-mail e senha temporária. Matrícula e e-mail são únicos na instituição.
- O primeiro acesso exige troca da senha temporária. Depois, o leitor pode alterar seu e-mail e senha.
- Login: um campo para e-mail ou matrícula e outro para senha.
- Na primeira versão, recuperação de acesso exige nova senha temporária criada pelo administrador; não há e-mail.
- O sistema pode sugerir senha aleatória criptograficamente segura.

## 3. Acervo

- O catálogo agrupa cópias equivalentes por título. Depois de escolher o título, o leitor pode escolher entre os exemplares disponíveis quando seus estados de conservação forem diferentes.
- Cada exemplar físico possui código único e estado próprio: disponível, reservado, emprestado, danificado, em manutenção, perdido ou descartado.
- O leitor pode comparar o estado dos exemplares, mas não precisa ver seus códigos internos.
- Toda concessão associa o exemplar escolhido ou, quando não houver escolha, um exemplar compatível específico.
- O administrador pode alterar ou restaurar qualquer estado; a ação é auditada.

### Dados bibliográficos

- **Obrigatórios:** título, autor, editora, edição, ano, categoria, descrição e capa principal.
- **Opcionais:** ISBN, número de páginas e imagens adicionais.
- Busca: título, autor, ISBN, categoria, todo o texto da descrição e tags como `#medieval`.
- Na devolução, o leitor pode sugerir novas tags que caracterizem o título. Cada sugestão deve preservar autoria e data para rastreabilidade.
- Filtros: disponibilidade, avaliação e ano.

### Imagens

- Na primeira versão, arquivos ficam em diretório persistente no VPS; PostgreSQL guarda caminhos, metadados e relações.
- A abstração de armazenamento do Django deve permitir migração futura para um serviço de objetos.

## 4. Calendário e políticas

O administrador configura:

- dias regulares de funcionamento, inicialmente segunda a sexta-feira;
- feriados e fechamentos;
- prazo do empréstimo, inicialmente entre 3 e 15 dias de funcionamento;
- limite simultâneo, inicialmente 3 empréstimos;
- tolerância para retirada, inicialmente 1 dia de funcionamento;
- penalidades por atraso e cancelamentos frequentes;
- permissão para renovação;
- suspensão de novas reservas sem afetar as confirmadas.

Somente dias de funcionamento contam nos prazos, exceto penalidades explicitamente definidas em dias corridos.

## 5. Reservas, empréstimos e fila

### Solicitação

1. Todo empréstimo começa com reserva, mesmo havendo disponibilidade imediata.
2. O leitor escolhe retirada e devolução dentro do calendário e das políticas.
3. O sistema valida elegibilidade, limite, período e disponibilidade.
4. Se permitido, concede sem confirmação administrativa e associa um exemplar; se recusar, explica o impedimento.

### Disponibilidade e prioridade

- Um exemplar não pode ter períodos confirmados sobrepostos.
- Sem disponibilidade, o leitor pode escolher período futuro.
- A fila é FIFO: a solicitação mais antiga tem prioridade.
- O leitor vê sua posição e datas estimadas, nunca a identidade de outras pessoas.
- A ordem da fila só pode mudar por nova decisão explícita de produto.

### Retirada não realizada e antecipação

- Quem não retirar dentro da tolerância perde a exclusividade sobre o período liberado, mas sua reserva não é cancelada imediatamente.
- Enquanto nenhum período conflitante for concedido a outra pessoa e houver exemplar disponível, o leitor original ainda pode retirar com atraso.
- O próximo leitor é avisado ao entrar no sistema e pode aceitar ou recusar retirada antecipada até a data original de sua reserva.
- Se aceitar, pode retirar antes e manter a devolução original, mesmo excedendo excepcionalmente o prazo máximo.
- Se recusar, preserva integralmente sua reserva.
- O período livre pode ser reservado por outra pessoa. Nesse caso, o leitor original é avisado pelo sistema, perde o direito ao intervalo conflitante e deve escolher novas datas.

### Alteração, cancelamento e renovação

- Antes da retirada, o leitor pode alterar ambas as datas ou cancelar, sem conflito com períodos confirmados.
- Após a retirada, pode apenas prorrogar a devolução, se não houver fila e respeitar o prazo máximo.
- O administrador pode visualizar, alterar e cancelar qualquer reserva ou empréstimo.

### Cancelamentos frequentes

- Padrão: até 3 cancelamentos do leitor em janela exata de 30 dias iniciada no primeiro cancelamento relevante.
- Ao ultrapassar o limite, novas solicitações são bloqueadas até o fim da janela; reservas confirmadas permanecem.
- Cancelamentos administrativos não contam. Limite, janela e penalidade são configuráveis.

## 6. Atrasos e penalidades

- Leitor com empréstimo atrasado não pode criar reservas.
- Padrão após atraso: bloquear novos empréstimos e reservas por 7 dias corridos.
- O administrador configura duração, suspensão e eventual redução do limite simultâneo.
- Reservas confirmadas não são alteradas retroativamente, salvo ação administrativa explícita e auditada.

## 7. Devolução e avaliações

- A cada devolução, o leitor pode avaliar separadamente conteúdo do título e estado do exemplar, de 1 a 5 estrelas.
- Avaliações são opcionais, independentes por devolução e não editáveis pelo leitor após o envio.
- Médias do título e do exemplar derivam das respectivas avaliações individuais, que são a fonte de verdade.

## 8. Auditoria e histórico

- Alterações administrativas relevantes em operações, estados e configurações geram registros persistentes.
- Registro: autor, data/hora, ação, valor anterior e novo; justificativa opcional.
- Auditoria não pode ser editada nem apagada por operações administrativas comuns.
- Históricos de empréstimos e auditoria são preservados.
- Reservas, retiradas, devoluções, cancelamentos, avaliações, alterações de estado e tags sugeridas devem manter data e relações históricas suficientes para análises futuras, como popularidade por período, preferência por categoria e estimativa da vida útil de exemplares. Não é necessário criar tabelas de estatísticas antecipadamente.
- Exclusão ou anonimização de leitores preserva integridade referencial e auditoria.
- Tokens expirados são removidos periodicamente; dados sintéticos de teste podem ser recriados.

## 9. Escopo da primeira versão

### Incluído

- Frontend React responsivo e internacionalizado.
- Backend com autenticação, autorização, usuários, acervo, reservas, empréstimos, fila, calendário, políticas, penalidades, avaliações, avisos internos e auditoria.
- Painéis de leitor e administrador; catálogo, busca, filtros e disponibilidade futura.
- Persistência relacional e mensagem de backend indisponível sem indicar sucesso indevido.

### Futuro

- Envio por e-mail dos avisos de antecipação e perda de prioridade. Na primeira versão, esses avisos já aparecem ao entrar no sistema.
- Recuperação autônoma de senha por e-mail.
- Leitores ópticos, scanners ou totens para registrar retirada e devolução físicas sob as mesmas regras e auditoria da API.

## 10. Experiência e acessibilidade

- Interface moderna, minimalista, bela e funcional em computadores e smartphones.
- Português do Brasil e inglês; seleção inicial pelo idioma do navegador e escolha manual persistente. Não usar geolocalização por IP.
- Meta WCAG 2.2 AA, com testes automatizados e revisão manual.
- Cobrir teclado, foco, contraste, semântica, leitor de tela, texto alternativo, formulários, toque, zoom/reflow, movimento reduzido e gerenciadores de senha.
- Estados essenciais: carregamento, vazio, erro, sucesso e backend indisponível.

### Temas

Todos os componentes usam tokens semânticos; o tema é escolhido em um único ponto. Cor nunca é o único indicador de estado.

| Tema | Primária | Secundária | Destaque | Fundo | Intenção |
|---|---|---|---|---|---|
| 1. Calculus | `#111827` | `#8B6F47` | `#D9CCB4` | `#FAF9F6` | acadêmico e sóbrio |
| 2. Oceano e cobre | `#0F3D3E` | `#285E61` | `#B66A3C` | `#F4F7F6` | moderno e institucional |
| 3. Vinho e ouro | `#3B1021` | `#6B213C` | `#A67C32` | `#FBF7EF` | clássico e acolhedor |
| 4. Ardósia e sálvia | `#243447` | `#496273` | `#667B68` | `#F5F7F2` | discreto e contemporâneo |
| 5. Índigo e âmbar | `#1E1B4B` | `#3730A3` | `#B45309` | `#F8FAFC` | digital e expressivo |
| 6. Aqua Glass | `#0B3B60` | `#1677A6` | `#67D4E8` | `#EAF7FB` | aquático e translúcido |

O Tema 1 referencia [First Principles of Calculus](https://mlee-code.github.io/First-Principles-of-Calculus/). Tokens completos serão derivados para `UX_UI.md`. O Tema 6 exige fallback opaco e não pode prejudicar contraste, legibilidade nem preferências de redução de transparência e movimento.

## 11. Arquitetura e segurança

- **Frontend:** React, `HashRouter`, endereço padrão do GitHub Pages.
- **Backend:** Python, Django e Django REST Framework em VPS da Hostinger, executado sob demanda.
- **Banco:** PostgreSQL via Django ORM.
- **Comunicação:** API HTTPS; CORS restrito à origem exata do frontend.
- Priorizar recursos gratuitos; serviço pago exige aprovação.

### Backup

- PostgreSQL e diretório de imagens devem ser copiados como um conjunto consistente, com manifesto e verificações de integridade.
- Os backups devem ser criptografados e mantidos fora do VPS, inicialmente em repositório controlado pelo responsável.
- Criar backup antes de mudanças de infraestrutura e, quando o backend estiver em uso, uma cópia diária com retenção inicial de 7 diárias e 4 semanais.
- Testar a restauração antes de cada entrega relevante e registrar o resultado; backup sem restauração verificada não conta como proteção válida.

### Autenticação

- Backend emite token bearer opaco, aleatório, revogável e de curta duração.
- React mantém token somente em memória e o envia em `Authorization`; proibir persistência no navegador.
- Backend armazena apenas representação segura. Recarregar a página pode exigir login.
- Sessão expira após 30 minutos de inatividade ou 8 horas absolutas.
- Logout, expiração e troca/recuperação de senha invalidam credenciais aplicáveis.
- Senhas: mínimo 15 caracteres; aceitar ao menos 64, espaços e Unicode normalizado.
- Não exigir composição artificial; bloquear senhas comuns/comprometidas e oferecer medidor de força.
- Usar hash seguro do framework e limitar tentativas de login.
- Nunca expor ou registrar senhas, tokens reutilizáveis, credenciais do banco ou dados pessoais desnecessários.

## 12. Dados, compatibilidade e escala

- Dados pessoais de demonstração e teste são sintéticos.
- Metadados e capas reais só quando legalmente permitidos; respeitar direitos e licenças.
- Compatibilidade: duas versões estáveis mais recentes de Chrome, Firefox, Edge e Safari na entrega.
- Meta simulada: 5.000 leitores, 20.000 títulos, 50.000 exemplares e pico de 500 usuários simultâneos por instalação.

## 13. Qualidade e aceite

### Testes

- Unitários: regras, validações, calendários, filas e penalidades.
- Integração: API, autenticação, autorização, ORM, PostgreSQL e concorrência.
- Contrato entre React e API; componentes e acessibilidade; ponta a ponta; segurança; carga simulada.

### Primeira versão pronta quando

- Perfis executarem somente ações autorizadas e os fluxos de acesso funcionarem.
- Administrador gerenciar leitores, acervo, calendário, políticas e operações.
- Leitor pesquisar, reservar, acompanhar, alterar, cancelar, renovar quando permitido e avaliar.
- Filas, prazos, limites e penalidades não provocarem sobreposição de exemplar.
- Auditoria funcionar sem expor segredos.
- Interface funcionar nos dois idiomas e dispositivos, com evidências de WCAG 2.2 AA.
- Frontend publicado consumir a API por HTTPS e informar indisponibilidade.
- Testes aplicáveis e simulação de carga passarem com resultados registrados.
- Nenhum segredo nem dado pessoal real estiver versionado.

## 14. Riscos e pendências

### Riscos

- O deploy depende de VPS Hostinger adequado e pode gerar custo e administração operacional.
- A comunicação entre GitHub Pages e VPS depende de HTTPS, CORS e configuração correta.
- Backend desligado torna funções dinâmicas indisponíveis; isso é intencional e deve ser explicado na interface.

### Decisões consolidadas nesta revisão

- Uma reserva só se torna empréstimo ativo na confirmação da retirada física do exemplar.
- Avisos de antecipação e perda do período são exibidos ao leitor quando ele entra no sistema; e-mail permanece futuro.
- ISBN é opcional e avaliações válidas usam de 1 a 5 estrelas.
- O modelo persistirá eventos e relações históricas para permitir análises futuras sem pré-calcular estatísticas.
- Backups consistentes do banco e das imagens serão criptografados, mantidos fora do VPS e terão restauração testada.
