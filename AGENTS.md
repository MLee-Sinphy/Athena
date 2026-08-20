# Athena — Instruções para agentes

Estas instruções se aplicam a todo o repositório.

## Processo de desenvolvimento

- Siga o Processo de Desenvolvimento Assistido por IA adotado pelo projeto.
- Trate `workspace/PROJECT_CONTEXT.md` e `workspace/REVIEWS.md` como entradas humanas.
- Trate `docs/` como documentação oficial depois de validada pelo responsável.
- Não implemente decisões estratégicas ainda pendentes nem transforme hipóteses em requisitos silenciosamente.
- Antes da primeira implementação, conclua a documentação oficial, obtenha validação humana e defina tarefas e portões em `docs/TASKS.md` e `docs/TESTS.md`.

## Git e versionamento

- Faça commit após cada alteração relevante e coerente, depois de executar as validações aplicáveis.
- Faça push de cada commit relevante para a branch remota correspondente. Não deixe trabalho importante apenas localmente.
- Não crie commits vazios e não faça commit quando nenhuma alteração material tiver sido realizada.
- Use mensagens no padrão Conventional Commits, como `docs:`, `feat:`, `fix:`, `test:`, `refactor:` e `chore:`.
- Mantenha `main` como branch estável e integrável.
- Desenvolva documentação em `docs/project-documentation` enquanto esta fase estiver ativa.
- Para implementação futura, crie branches curtas por mudança, usando prefixos como `feat/`, `fix/`, `refactor/`, `test/` ou `chore/`.
- Não faça push forçado nem reescreva histórico compartilhado sem autorização explícita.
- Não versione segredos, credenciais, tokens, senhas, arquivos de ambiente reais ou dados pessoais.
- Revise `git status`, o diff e as verificações aplicáveis antes de cada commit.

## Versões e entregas

- Use Versionamento Semântico para versões entregues: `MAJOR.MINOR.PATCH`.
- Incremente `MAJOR` para mudanças incompatíveis, `MINOR` para capacidades compatíveis e `PATCH` para correções compatíveis.
- Crie tags de versão somente para entregas reais validadas; não use tags para planos ou documentação ainda não entregue.
- Mantenha `docs/CHANGELOG.md` alinhado às entregas reais e nunca registre como concluído algo apenas planejado.
