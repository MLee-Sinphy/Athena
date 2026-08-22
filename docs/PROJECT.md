# PROJECT.md

> Fonte oficial de identidade e direção estratégica do Athena. Derivada do contexto humano e sujeita à validação do responsável antes da implementação.

## Identidade
- Nome do projeto: Athena.
- Descrição curta: sistema web configurável para empréstimo gratuito de livros físicos.
- Estado atual: candidata funcional implementada; demonstração operacional validada e versão 1.0.0 ainda em validação final.

## Validação
- Aprovada por M Lee em 2026-08-22.
- A implementação deve seguir `TASKS.md` e os portões de `TESTS.md`.

## Visão
Oferecer a diferentes tipos de biblioteca uma experiência previsível de consulta, reserva e empréstimo, mantendo controle preciso de cada exemplar físico.

## Missão
Construir, como objeto de estudo, um sistema full stack documentado, testável e implantável que reúna frontend, API, autenticação, regras de negócio e persistência relacional.

## Filosofia
- Regras explícitas e configuráveis, sem hipóteses silenciosas.
- Experiência simples para o leitor e controle detalhado para o administrador.
- Privacidade, acessibilidade, segurança e rastreabilidade desde o desenho.
- Implementação incremental guiada por documentação e testes validados.

## Problema
Leitores precisam localizar livros e planejar períodos de uso; bibliotecas precisam controlar disponibilidade futura, filas, penalidades e o exemplar físico entregue, sem depender de registros dispersos ou políticas rígidas.

## Contexto
Cada implantação atende uma escola, universidade, biblioteca pública ou instituição semelhante. A entrega e a devolução continuam físicas. O backend pode operar somente durante sessões de estudo ou demonstração.

## Público-alvo
### Público principal
Leitores cadastrados pela instituição.

### Públicos secundários
Administradores responsáveis por usuários, acervo, calendário, políticas e operações.

## Necessidades do público
- Leitor: pesquisar títulos, comparar exemplares por conservação, escolher datas, reservar, acompanhar fila e administrar suas operações sem ver dados alheios.
- Administrador: identificar exemplares, cadastrar pessoas e acervo, configurar regras, intervir em operações e consultar histórico auditável.

## Soluções atuais
O projeto não possui uma instituição-alvo analisada. Parte do cenário plausível de atendimento presencial apoiado por registros manuais, planilhas ou sistemas pouco configuráveis.

## Limitações das soluções atuais
- Baixa visibilidade da disponibilidade futura.
- Controle fragmentado de títulos, exemplares, reservas e empréstimos.
- Dificuldade de adaptar prazos, calendários e penalidades.

## Proposta de valor
Agrupar o catálogo por título para simplificar a descoberta, conservar o controle individual dos exemplares e permitir que cada instituição ajuste sua política de empréstimo.

## Diferenciais
- Reserva por intervalo e disponibilidade futura.
- Escolha opcional de exemplar conforme seu estado físico.
- Fila cronológica e privada.
- Políticas administrativas configuráveis.
- Histórico preparado para análises futuras sem agregações prematuras.

## Objetivos
### Objetivo principal
Entregar a primeira versão funcional de ponta a ponta enquanto o backend estiver ativo.

### Objetivos secundários
- Exercitar React, Django, PostgreSQL, segurança, internacionalização, acessibilidade, testes e deploy.
- Produzir documentação e implementação rastreáveis como referência de estudo.
- Demonstrar o comportamento com dados sintéticos e carga simulada.

## Escopo inicial
- Dois perfis: leitor e administrador.
- Autenticação, primeiro acesso e recuperação assistida.
- Catálogo, títulos, exemplares, busca, tags e avaliações.
- Reservas, retirada, empréstimos, devolução, fila e avisos internos.
- Calendário, políticas, penalidades e auditoria.
- Interface responsiva em português e inglês.
- React no GitHub Pages; Django/DRF e PostgreSQL em VPS Hostinger.

## Fora de escopo
- Pagamentos e aluguel comercial.
- Conteúdo digital.
- E-mails na primeira versão.
- Autoatendimento por hardware.
- Múltiplas instituições na mesma implantação.
- Disponibilidade contínua ou SLA comercial.

## Critérios gerais de sucesso
- Jornadas essenciais funcionam somente para perfis autorizados.
- Nenhum exemplar possui períodos confirmados sobrepostos.
- Regras configuráveis possuem testes automatizados.
- Interface responsiva, bilíngue e com evidências de WCAG 2.2 AA.
- Indisponibilidade do backend é clara e nunca aparenta sucesso.
- Metas de escala são exercitadas por simulação reproduzível.

## Riscos estratégicos
- Complexidade do calendário, fila e concorrência.
- Custo e administração do VPS.
- Uso indevido de dados pessoais ou materiais bibliográficos protegidos.
- Escopo amplo para um projeto de estudo.

## Hipóteses importantes
- Um VPS adequado estará disponível para demonstração.
- Usuários aceitam novo login após recarregar a aplicação, pois o token não persiste no navegador.
- A instituição mantém códigos únicos nos exemplares e confirma fisicamente retirada e devolução.

## Dependências externas
- GitHub Pages.
- VPS Hostinger com HTTPS.
- PostgreSQL.
- Navegadores modernos.
