# Instruções obrigatórias para agentes

Antes de qualquer alteração neste repositório, leia e siga integralmente `AI-TO-CLI-PROTOCOL.md`.

A política é obrigatória para agentes de código, automações e IAs. Nenhuma alteração válida da tarefa pode ser abandonada sem merge validado na branch de destino.

## Isolamento obrigatorio de sessao CLI por chat

Antes de qualquer operacao em terminal/CLI, leia e cumpra a secao `Isolamento obrigatorio de sessao CLI por chat` de `AI-TO-CLI-PROTOCOL.md`. Cada chat deve usar sessao/namespace CLI exclusivo; reutilizacao de sessao entre chats e proibida. Estado necessario para retomada deve ser persistido fora da memoria do shell.
