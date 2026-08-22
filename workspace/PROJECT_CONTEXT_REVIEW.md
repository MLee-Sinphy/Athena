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

- O leitor primeiro vê um único título. Se houver exemplares em estados de conservação diferentes, pode comparar esses estados e escolher qual exemplar deseja.
- O sistema e o administrador controlam cada exemplar por código e estado próprios.
- Estados: disponível, reservado, emprestado, danificado, em manutenção, perdido ou descartado.
- Busca por título, autor, ISBN, categoria, todo o texto da descrição e tags como `#medieval`; filtros por disponibilidade, avaliação e ano.
- Na devolução, o leitor pode sugerir novas tags para caracterizar o título.
- Dados obrigatórios: título, autor, editora, edição, ano, categoria, descrição e capa. ISBN é opcional.
- Depois da devolução, o leitor pode dar notas independentes de 1 a 5 para o conteúdo e para o estado do exemplar.

## 4. Reserva e empréstimo

1. Todo empréstimo começa por uma reserva, mesmo com exemplar disponível.
2. O leitor escolhe retirada e devolução em dias de funcionamento.
3. O sistema aprova automaticamente se leitor, período, limite e disponibilidade estiverem regulares.
4. Um exemplar específico é separado sem exigir confirmação do administrador.
5. A reserva só se torna empréstimo ativo quando a retirada física for confirmada.
6. Sem disponibilidade, o leitor escolhe um período futuro e entra em fila por ordem de solicitação.
7. A fila mostra posição e previsão, nunca dados dos outros leitores.

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

Se uma reserva ultrapassar a tolerância sem retirada ou um livro voltar antes:

- o leitor atrasado perde a exclusividade, mas ainda pode retirar se o exemplar continuar livre e não surgir conflito;
- o próximo da fila recebe um aviso ao entrar, mantém sua reserva original e pode antecipar a retirada conservando a devolução original;
- se o próximo não antecipar, outra pessoa pode reservar o período livre;
- se isso ocorrer, o leitor atrasado recebe um aviso, perde o intervalo conflitante e deve escolher novas datas.

E-mails serão futuros. Os avisos internos descritos acima fazem parte da primeira versão. Recuperação de senha por e-mail e retirada/devolução com scanner também ficam para o futuro.

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
- Banco e imagens terão backup conjunto, criptografado e fora do VPS, com retenção de 7 cópias diárias e 4 semanais e testes de restauração antes de entregas relevantes.
- Testes automatizados e dados pessoais fictícios; escala simulada de até 5.000 leitores, 20.000 títulos, 50.000 exemplares e 500 acessos simultâneos.

## 9. Dados para análises futuras

O sistema preservará datas e relações de reservas, retiradas, devoluções, cancelamentos, avaliações, estados físicos e tags. Isso permitirá calcular futuramente, sem tabelas estatísticas prematuras:

- quantidade de empréstimos por título e período;
- categorias e estilos mais procurados;
- evolução das avaliações;
- frequência de danos e estimativa de vida útil dos exemplares.

## 10. Decisões confirmadas nesta revisão

- O leitor pode escolher um exemplar pelo estado de conservação.
- Descrição e tags participam da busca; leitores podem sugerir tags na devolução.
- A reserva vira empréstimo somente na retirada física.
- Avisos de antecipação e perda do período aparecem ao entrar no sistema.
- ISBN é opcional; notas válidas vão de 1 a 5.
- A estratégia de backup será detalhada tecnicamente pelo projeto.

## 11. Confirmação geral

Confirme se o objetivo, os perfis, o fluxo, os padrões configuráveis e as decisões desta revisão representam corretamente o produto que você deseja construir.
