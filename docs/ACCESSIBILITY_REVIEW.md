# ACCESSIBILITY_REVIEW.md

> Revisão incremental do GATE-007 em 2026-08-22. A matriz final de navegadores e tecnologias assistivas permanece no GATE-008.

## Escopo
Login, preferências, catálogo, reservas, empréstimos, avisos, perfil e formulários administrativos, em 320 × 700 e 1440 × 900.

## Evidência automatizada
- Axe Core não encontrou violações estruturais na tela pública renderizada.
- Playwright concluiu login e acesso ao catálogo nos dois viewports sem rolagem horizontal da página.
- Testes verificam rótulos, regiões semânticas, mensagens vivas, equivalência dos catálogos pt-BR/en e persistência das preferências.
- Contraste de texto/fundo e botão primário foi calculado para as seis paletas com limite mínimo 4,5:1.

## Revisão do código e da interação
- Link de salto torna-se visível ao foco; cabeçalho, navegação e conteúdo principal possuem regiões identificáveis.
- Todos os campos possuem rótulo; senha usa `autocomplete`; erros e sucessos usam `alert` ou `status`.
- Foco visível não depende de cor de fundo e os alvos interativos possuem altura mínima de 44 px.
- Navegação do leitor comunica a seção atual com `aria-current`; avisos não dependem apenas da cor.
- Layout mobile mantém funções e conteúdo; desktop muda a navegação para barra lateral sem duplicá-la.
- Movimento e transparência possuem redução; Aqua Glass conserva superfície opaca como fallback.

## Pendências para aceite final
- Executar a matriz manual nas duas versões estáveis dos navegadores alvo disponíveis.
- Validar NVDA/Firefox, VoiceOver/Safari e ampliação de 200–400% no ambiente de homologação.
- Repetir Axe e inspeção de contraste com dados reais e todas as telas administrativas.
