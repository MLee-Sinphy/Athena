# Athena — resumo para validação

> Este é o texto curto para revisão humana. Corrija aqui o que estiver errado ou incompleto; depois as correções serão incorporadas ao contexto-base e à documentação oficial.

## 1. Proposta

Athena é um projeto de estudo: um sistema web configurável para empréstimo gratuito de livros físicos em escolas, universidades e bibliotecas. Cada instalação atende uma única instituição. O sistema funciona quando o backend estiver ligado; se ele estiver inacessível, o frontend deve explicar isso claramente.

Não haverá pagamentos, livros digitais nem exigência de funcionamento contínuo.

## 2. Pessoas e permissões

- **Leitor:** pesquisa títulos e gerencia suas próprias reservas e empréstimos dentro das regras.
- **Administrador:** cadastra leitores e acervo, configura todas as políticas e pode visualizar, alterar ou cancelar qualquer operação. Mudanças relevantes são auditadas.
- O administrador cria a conta com matrícula, e-mail e senha temporária; o primeiro acesso exige nova senha.
- Login por e-mail ou matrícula. Recuperação inicial de acesso é assistida pelo administrador, sem e-mail.

## 3. Acervo e catálogo

- O leitor vê um único título mesmo quando existem várias cópias.
- O sistema e o administrador controlam cada exemplar por código e estado próprios.
- Estados: disponível, reservado, emprestado, danificado, em manutenção, perdido ou descartado.
- Busca por título, autor, ISBN, categoria, descrição e palavras-chave; filtros por disponibilidade, avaliação e ano.
- Dados hoje definidos como obrigatórios: título, autor, ISBN, editora, edição, ano, categoria, descrição e capa.
- Depois da devolução, o leitor pode dar notas independentes de 0 a 5 para o conteúdo e para o estado do exemplar.

## 4. Reserva e empréstimo

1. Todo empréstimo começa por uma reserva, mesmo com exemplar disponível.
2. O leitor escolhe retirada e devolução em dias de funcionamento.
3. O sistema aprova automaticamente se leitor, período, limite e disponibilidade estiverem regulares.
4. Um exemplar específico é separado sem exigir confirmação do administrador.
5. Sem disponibilidade, o leitor escolhe um período futuro e entra em fila por ordem de solicitação.
6. A fila mostra posição e previsão, nunca dados dos outros leitores.

Antes da retirada, o leitor pode alterar ambas as datas ou cancelar sem prejudicar reservas confirmadas. Depois da retirada, só pode prorrogar a devolução se não houver fila e se respeitar o prazo máximo.

## 5. Padrões configuráveis

Estes são apenas valores iniciais; o administrador poderá alterá-los no painel:

| Regra | Padrão atual |
|---|---|
| Funcionamento | segunda a sexta, com feriados e fechamentos cadastráveis |
| Prazo | mínimo 3 e máximo 15 dias de funcionamento |
| Limite simultâneo | 3 empréstimos |
| Tolerância para retirada | 1 dia de funcionamento |
| Atraso | bloqueio de novos empréstimos e reservas por 7 dias corridos |
| Cancelamentos | até 3 em uma janela de 30 dias |
| Excesso de cancelamentos | bloqueia novas solicitações até o fim da janela |

Reservas já confirmadas são preservadas pelas penalidades automáticas. Leitor com devolução atrasada não pode criar reserva.

## 6. Vaga liberada antes do previsto

Se uma reserva expirar sem retirada ou um livro voltar antes:

- o próximo da fila mantém sua reserva original;
- pode optar por retirar antes e conservar a devolução original, mesmo que isso exceda excepcionalmente o prazo máximo;
- se não quiser antecipar, o período livre pode ser oferecido a outra pessoa sem afetar reservas existentes.

Notificações internas e por e-mail serão futuras, assim como recuperação de senha por e-mail e retirada/devolução com scanner ou leitor óptico.

## 7. Interface

- React responsivo para computador e celular, com visual moderno, minimalista e acessível.
- Português e inglês, inicialmente conforme o idioma do navegador e com troca manual.
- Meta WCAG 2.2 AA.
- Seis temas intercambiáveis por variáveis: acadêmico (paleta do site de cálculo), oceano/cobre, vinho/ouro, ardósia/sálvia, índigo/âmbar e Aqua Glass translúcido.

## 8. Arquitetura já escolhida

- React no endereço padrão do GitHub Pages.
- API Python com Django e Django REST Framework em VPS Hostinger, sob demanda.
- PostgreSQL e Django ORM.
- HTTPS e token de acesso mantido somente na memória do frontend; atualizar a página pode exigir novo login.
- Imagens inicialmente no VPS, com referências no banco e possibilidade de migração futura.
- Testes automatizados e dados pessoais fictícios; escala simulada de até 5.000 leitores, 20.000 títulos, 50.000 exemplares e 500 acessos simultâneos.

## 9. Pontos que precisam da sua avaliação

1. **Início do empréstimo:** a reserva se torna empréstimo ativo quando é aprovada, quando chega a data marcada ou somente quando o exemplar é fisicamente retirado?
2. **Antecipação na primeira versão:** sem notificações, como o próximo leitor saberá que pode retirar antes — aviso ao entrar no sistema, consulta manual em sua reserva ou essa antecipação deve ficar totalmente para uma versão futura?
3. **ISBN obrigatório:** ele deve continuar obrigatório mesmo para obras antigas, edições especiais ou itens que não tenham ISBN?
4. **Nota zero:** `0 estrelas` é uma avaliação válida ou deve representar apenas “não avaliado”, fazendo a menor nota válida ser `1 estrela`?
5. **Backup:** você quer decidir agora como salvar banco e imagens do VPS ou prefere delegar essa decisão técnica para `ARCHITECTURE.md`?

## 10. Confirmação geral

Além das cinco perguntas acima, confirme se o objetivo, os perfis, o fluxo, os padrões configuráveis e o escopo futuro representam corretamente o produto que você deseja construir.
