# UX_UI.md

> Direção de experiência validada pelo responsável em 2026-08-22. Protótipos e detalhes visuais ainda serão verificados nos portões correspondentes.

## Visão da experiência
Uma biblioteca digitalmente organizada, calma e confiável: descoberta simples para o leitor e densidade controlada no painel administrativo.

## Princípios de UX
- Mostrar títulos antes de detalhes operacionais.
- Explicar regras e impedimentos no contexto da ação.
- Nunca revelar dados de outros leitores.
- Preservar o trabalho do usuário em erros recuperáveis.
- Usar padrões consistentes em mobile e desktop.

## Sensação desejada
Moderna, minimalista, bela, acadêmica e acolhedora.

## Sensações que devem ser evitadas
Interface carregada, infantil, excessivamente animada, opaca sobre disponibilidade ou dependente apenas de cor.

## Público e contexto de uso
Leitores sem treinamento técnico e administradores com orientação inicial, em smartphones e computadores, inclusive durante atendimento presencial.

## Jornada principal do usuário
1. Entrar por e-mail ou matrícula. 2. Pesquisar ou explorar. 3. Abrir título e disponibilidade. 4. Comparar conservação se desejar. 5. Escolher datas. 6. Reservar ou entrar na fila. 7. Acompanhar avisos e operações. 8. Avaliar e sugerir tags após devolver.

## Arquitetura da informação
- Pública: login, primeiro acesso e indisponibilidade.
- Leitor: catálogo, título, calendário, minhas reservas/empréstimos, avisos, perfil.
- Administrador: visão geral, circulação, leitores, acervo, calendário/políticas, auditoria.

## Navegação
### Estrutura principal
Cabeçalho global; navegação inferior compacta no mobile do leitor; barra lateral recolhível no desktop administrativo.
### Comportamento
Rotas preservam filtros úteis; ações destrutivas exigem confirmação contextual; retorno mantém o ponto anterior quando possível.
### Navegação por teclado
Ordem lógica, skip link, foco visível, retorno correto após modal e nenhuma armadilha.

## Identidade visual
### Paleta de cores
Seis temas usam os mesmos tokens: `primary`, `secondary`, `accent`, `background`, `surface`, `text`, `muted`, `border`, `success`, `warning`, `error`, `info`, foco e estados interativos. Paletas-base estão em `PROJECT_CONTEXT.md`; Tema 1 é preferencial inicial e Tema 6 usa transparência com fallback opaco.
### Tipografia
Fonte de interface legível e livre; escala responsiva moderada; corpo mínimo equivalente a 16 px; números e códigos administrativos alinháveis.
### Espaçamentos
Escala base de 4 px, com ritmos principais de 8, 12, 16, 24, 32 e 48.
### Bordas e sombras
Raios moderados; sombra apenas para hierarquia; foco não depende de sombra. Aqua Glass usa blur discreto e desativável.

## Layout
### Mobile
Uma coluna, ações essenciais próximas ao polegar, tabelas administrativas transformadas em cartões ou rolagem explicitamente rotulada.
### Tablet
Uma ou duas colunas conforme conteúdo; painéis adaptam densidade.
### Desktop
Conteúdo central e painel com navegação lateral; comparação de exemplares pode usar colunas.
### Largura máxima de conteúdo
Leitura limitada aproximadamente a 80 caracteres; áreas operacionais podem alcançar 1440 px.

## Componentes
### Botões
Primário único por contexto; secundário, terciário e destrutivo; estados foco, hover, ativo, desabilitado e carregando.
### Campos de entrada
Rótulo sempre visível, ajuda associada e erro acionável. Login possui identificador e senha.
### Cards
Título mostra capa, metadados essenciais, avaliação e disponibilidade; exemplar mostra conservação sem expor código ao leitor.
### Navegação
Estado atual comunicado visual e semanticamente; menus operáveis por teclado.
### Modais
Somente para confirmação curta ou tarefa realmente bloqueante; preferir página ou painel para formulários extensos.

## Estados da interface
### Carregamento
Indicador com texto acessível; skeleton sem simular conteúdo enganoso.
### Vazio
Explica por que não há dados e oferece próxima ação.
### Erro
Mensagem humana, preserva entrada e indica correção ou nova tentativa.
### Sucesso
Confirma resultado e estado atualizado sem depender apenas de toast.
### Desabilitado
Usar somente quando o motivo estiver visível; quando útil, permitir ação e explicar impedimento.
### Backend indisponível
Banner ou tela clara: serviço temporariamente inacessível, nenhuma operação concluída, ação para tentar novamente.

## Animações
Curtas, funcionais e dispensáveis; respeitar `prefers-reduced-motion`.

## Responsividade
Projetar mobile-first; testar larguras de 320 px até desktop amplo; nenhuma função essencial ou informação crítica desaparece.

## Acessibilidade
Meta WCAG 2.2 AA: contraste, zoom/reflow, alvos, foco, teclado, semântica, leitores de tela, mensagens de estado, textos alternativos, autocomplete, colagem e gerenciadores de senha. Avaliar os seis temas por automação e revisão humana.

## Referências
- First Principles of Calculus para a paleta acadêmica.
- `REQ-NF-004`, `REQ-NF-005`, `REQ-NF-006`, `REQ-NF-012`.

## Anti-referências
- Glassmorphism com contraste insuficiente.
- Calendários que não expliquem dias fechados.
- Fila que revele identidades.

## Observações adicionais
Wireframes e componentes detalhados serão produzidos na tarefa de design e validados antes da implementação visual completa.
