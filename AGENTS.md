# Instruções obrigatórias para agentes

Antes de qualquer alteração neste repositório, leia e siga integralmente `AI-TO-CLI-PROTOCOL.md`.

A política é obrigatória para agentes de código, automações e IAs. Nenhuma alteração válida da tarefa pode ser abandonada sem merge validado na branch de destino.

## Isolamento obrigatorio de sessao CLI por chat

Antes de qualquer operacao em terminal/CLI, leia e cumpra a secao `Isolamento obrigatorio de sessao CLI por chat` de `AI-TO-CLI-PROTOCOL.md`. Cada chat deve usar sessao/namespace CLI exclusivo; reutilizacao de sessao entre chats e proibida. Estado necessario para retomada deve ser persistido fora da memoria do shell.
## Auditoria Extrema — cobertura universal obrigatória

Quando houver auditoria completa/extrema, validação de release/apto ou gatilho de `AUDIT_POLICY.md`, execute integralmente `AUDIT_POLICY.md`, `docs/quality/EXTREME_AUDIT_PROTOCOL.md`, `docs/quality/AUDIT_RUNTIME_PARITY_V1.md`, `docs/quality/AUDIT_UNIVERSAL_COVERAGE_V1.md`, `docs/quality/AUDIT_SELF_TEST_V1.md` quando aplicável e `docs/quality/AUDIT_OVERLAY.md`. Corrija achados SAFE, procure falhas silenciosas/órfãos/flaky/unknown unknowns e não encerre em relatório sem remediação.

## Auditoria de arquitetura/deploy
Em Auditoria Extrema, leia e execute também `docs/quality/ARCHITECTURE_DEPLOY_AUDIT_V1.md`. Avalie caminho crítico de CI/deploy, runners, build/artifact, cache, provisionamento/restarts, migrations, contratos cross-repo, ownership de dados, workflow sprawl, hotspots e rollback.
