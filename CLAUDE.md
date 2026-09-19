# Instrucoes para Claude


<!-- SUPERPOWERS_EVERY_STAGE_V1 -->
> **@Superpowers CONTÍNUO E OBRIGATÓRIO:** toda conversa, sessão, agente e retomada de tarefa ShopVivaliz deve usar @Superpowers **em cada etapa material**, não apenas no início. Reaplique a disciplina adequada ao passar por bootstrap/contexto, planejamento, investigação, coleta de evidências, implementação, debugging, TDD/testes, revisão, correção, PR/checks/merge, deploy, pós-deploy, auditoria e encerramento. Em `retome/continue/prossiga`, continue do último checkpoint comprovado sob @Superpowers. Se o runtime não expuser @Superpowers, registre `SUPERPOWERS_UNAVAILABLE` e aplique a metodologia equivalente sem fingir a chamada. Fonte local: `REGRAS-AGENTES-CENTRALIZADAS.md`; fonte canônica: `Vivaliz-site/site-shopvivaliz`.

Antes de qualquer trabalho neste repositorio, leia e cumpra `AGENTS.md` e `AI-TO-CLI-PROTOCOL.md`. A regra `Isolamento obrigatorio de sessao CLI por chat` e vinculante: este chat nao pode reutilizar sessao CLI pertencente a outro chat.

Em Auditoria Extrema, também é obrigatório executar `AUDIT_POLICY.md`, `docs/quality/EXTREME_AUDIT_PROTOCOL.md`, `docs/quality/AUDIT_RUNTIME_PARITY_V1.md`, `docs/quality/AUDIT_UNIVERSAL_COVERAGE_V1.md`, `docs/quality/AUDIT_SELF_TEST_V1.md` quando aplicável e `docs/quality/AUDIT_OVERLAY.md`.

## Auditoria de arquitetura/deploy
Em Auditoria Extrema, leia e execute também `docs/quality/ARCHITECTURE_DEPLOY_AUDIT_V1.md`. Avalie caminho crítico de CI/deploy, runners, build/artifact, cache, provisionamento/restarts, migrations, contratos cross-repo, ownership de dados, workflow sprawl, hotspots e rollback.
