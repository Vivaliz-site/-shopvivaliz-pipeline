<!-- AUDIT_EXTERNAL_REMEDIATION_V1 -->
> **AUDITORIA EXTERNA TAMBÉM É CORRETIVA:** auditoria interna, externa, independente, contraditória ou feita por outro agente/revisor segue o mesmo ciclo. Auditor externo com autorização deve corrigir, testar e reauditar. Se for read-only, o relatório não encerra: os achados corrigíveis seguem para executor autorizado e permanecem em andamento até correção + revalidação independente ou bloqueio externo comprovado.
<!-- /AUDIT_EXTERNAL_REMEDIATION_V1 -->
<!-- AUDIT_REMEDIATE_VALIDATE_GLOBAL_V1 -->
## Auditoria corretiva obrigatória

- Todo pedido de auditoria significa **investigar, corrigir, prevenir e validar**; não encerrar apenas relacionando erros.
- Todo achado material corrigível e autorizado deve ter causa raiz investigada, correção aplicada, prevenção pertinente, teste e reauditoria.
- Relatório, recomendação, plano ou issue são estados intermediários enquanto existir ação segura executável.
- APTO/COMPROVADO/CONCLUIDO exigem evidência fresca pós-correção e E2E real quando aplicável; sem falso-verde.
- Pendência só é aceitável após esgotar alternativas seguras, com evidência, causa e ação exata necessária para continuidade.
- Fonte global: `REGRAS-AGENTES-CENTRALIZADAS.md`, policy `AUDIT_REMEDIATE_VALIDATE_GLOBAL_V1`.
<!-- /AUDIT_REMEDIATE_VALIDATE_GLOBAL_V1 -->

<!-- SHOPVIVALIZ_REMOTE_ACCESS_V1 -->
## Acesso remoto obrigatório para agentes

Antes de qualquer operação em VM, runtime, navegador, serviço, deploy, logs ou recuperação, leia **`docs/AGENT-REMOTE-ACCESS.md`**. O padrão vigente é SSH privado/Tailscale com `shopvivaliz-agent` para shell, RustDesk self-hosted para GUI, OCI Bastion/control plane auditável quando o ambiente não possui rota privada, e Desktop Commander somente como contingência. Navegador ShopVivaliz deve rodar na VM backend, nunca nos hosts Windows.

# Instruções obrigatórias para agentes

<!-- GLOBAL_BROWSER_VM_POLICY_V2 -->
> **NAVEGAÇÃO GLOBAL — VM OBRIGATÓRIA; WINDOWS PROIBIDO PARA BROWSER:** qualquer navegador, automação browser, sessão gráfica, Playwright/Selenium/CDP, Chrome/Chromium/Edge/Opera, CAPTCHA, MFA, consentimento ou validação visual deve usar por padrão e obrigatoriamente a VM backend `always-free-arm-1787907847-26` (`10.0.1.38`) e o Browser Worker privado. Para intervenção humana, usar `https://shopvivaliz.com.br/admin/browser-worker.php`. **Fred-Win (`LAPTOP-NIG4IFUU`) e `DESKTOP-KOCEPSV` não são destinos nem fallback para navegação.** Não perguntar qual máquina usar para browser: use a VM. Exceção somente se o proprietário ordenar explicitamente, na tarefa atual, o uso de um Windows específico para aquela navegação. Se a VM estiver indisponível, reparar o caminho VM/OCI Bastion/túnel privado ou registrar bloqueio real; nunca migrar silenciosamente para Windows. Workflows/relays Windows de browser são legado e não devem ser executados até serem migrados. A regra não proíbe Windows para tarefas não-browser que realmente dependam dele.

<!-- GLOBAL_BROWSER_SESSION_PROFILE_V1 -->
> **SESSAO CANONICA OPENAI/CHATGPT NA VM:** para qualquer navegacao em ChatGPT/OpenAI no Browser Worker, reutilize o contexto persistente existente com `persistent=true` e `profile=ai-squad-chatgpt`. Esse e o perfil canonico que deve preservar a autenticacao ja realizada. Nao criar perfil novo, nao usar `manual` como fallback e nao migrar para Fred-Win/KOCEPSV. Se a autenticacao expirar ou exigir MFA/CAPTCHA, abra **esse mesmo perfil** pela interface autenticada `https://shopvivaliz.com.br/admin/browser-worker.php`, conclua a autenticacao nele e continue reutilizando `ai-squad-chatgpt`. Labels/TTL de sessoes de trabalho podem variar, mas o profile para ChatGPT/OpenAI deve permanecer `ai-squad-chatgpt`, salvo ordem explicita do proprietario na tarefa atual.

<!-- FINAL_RESPONSE_DEPLOY_GATE_V1 -->
> **CONCLUSAO GLOBAL — MERGE NAO ENCERRA A TAREFA:** toda alteracao versionada deve seguir ate branch -> validacao -> PR -> checks -> merge e, quando o repositorio tiver alvo de deploy/runtime, deploy pelo gate canonico + validacao pos-deploy real. PR aberta, checks verdes ou merge isoladamente sao estados intermediarios. Antes de responder CONCLUIDO, o agente deve provar que o ramo alvo e o runtime/deploy aplicavel estao na revisao esperada e que nao restou PR da propria rodada. Se o deploy automatico pular, falhar ou ficar atrasado, o agente deve acionar o gate canonico e continuar ate paridade; so um bloqueio externo real e incontornavel permite encerrar como BLOQUEIO EXTERNO/INCONCLUSIVO.



<!-- SUPERPOWERS_EVERY_STAGE_V1 -->
> **@Superpowers CONTÍNUO E OBRIGATÓRIO:** toda conversa, sessão, agente e retomada de tarefa ShopVivaliz deve usar @Superpowers **em cada etapa material**, não apenas no início. Reaplique a disciplina adequada ao passar por bootstrap/contexto, planejamento, investigação, coleta de evidências, implementação, debugging, TDD/testes, revisão, correção, PR/checks/merge, deploy, pós-deploy, auditoria e encerramento. Em `retome/continue/prossiga`, continue do último checkpoint comprovado sob @Superpowers. Se o runtime não expuser @Superpowers, registre `SUPERPOWERS_UNAVAILABLE` e aplique a metodologia equivalente sem fingir a chamada. Fonte local: `REGRAS-AGENTES-CENTRALIZADAS.md`; fonte canônica: `Vivaliz-site/site-shopvivaliz`. Subagentes e automações delegadas herdam esta obrigação em todas as fases aplicáveis.

Antes de qualquer alteração neste repositório, leia e siga integralmente `AI-TO-CLI-PROTOCOL.md`.

A política é obrigatória para agentes de código, automações e IAs. Nenhuma alteração válida da tarefa pode ser abandonada sem merge validado na branch de destino.

## Isolamento obrigatorio de sessao CLI por chat

Antes de qualquer operacao em terminal/CLI, leia e cumpra a secao `Isolamento obrigatorio de sessao CLI por chat` de `AI-TO-CLI-PROTOCOL.md`. Cada chat deve usar sessao/namespace CLI exclusivo; reutilizacao de sessao entre chats e proibida. Estado necessario para retomada deve ser persistido fora da memoria do shell.
## Auditoria Extrema — cobertura universal obrigatória

Quando houver auditoria completa/extrema, validação de release/apto ou gatilho de `AUDIT_POLICY.md`, execute integralmente o conjunto V5 absoluto: `AUDIT_POLICY.md`, `docs/quality/EXTREME_AUDIT_PROTOCOL.md`, `docs/quality/AUDIT_RUNTIME_PARITY_V1.md`, `docs/quality/AUDIT_UNIVERSAL_COVERAGE_V1.md`, `docs/quality/ARCHITECTURE_DEPLOY_AUDIT_V1.md`, `docs/quality/AUDIT_SELF_TEST_V1.md`, `docs/quality/AUDIT_BROWSER_E2E_REAL_V1.md` quando houver UI, `docs/quality/AUDIT_JOURNEY_INVENTORY_V1.md`, `docs/quality/AUDIT_CLEAN_ROOM_REALITY_V1.md`, `docs/quality/AUDIT_HARDENING_MAX_V1.md`, `docs/quality/AUDIT_APTO_REMEDIATION_LOOP_V1.md`, `docs/quality/AUDIT_ESCAPE_INVALIDATION_V1.md`, `docs/quality/AUDIT_ABSOLUTE_GATE_V1.md`, `docs/quality/AUDIT_AUTH_CREDENTIAL_DISCOVERY_V1.md`, `docs/quality/AUDIT_MERGE_ENFORCEMENT_V1.md`, `docs/quality/AUDIT_PROJECT_REQUIREMENTS_V1.md`, o `docs/quality/AUDIT_PROJECT_REQUIREMENTS.json` local e `docs/quality/AUDIT_OVERLAY.md`. Antes de bloquear por login/credencial, o agente procura referências e mecanismos seguros em todos os repositórios governados e nos perfis/secret stores canônicos, sem expor valores. O próprio agente executa E2E real no browser, corrige todo bloqueador executável e repete auditoria/deploy/reauditoria até o certifier retornar `AUDIT_VERDICT=APTO`; somente bloqueio externo real permite `BLOCKED_EXTERNAL`. O `governance-gate` deve executar `scripts/absolute-audit-governance-validate.sh`; todo push em `main`/`master` deve passar pelo Absolute Audit Main Guard e provar associação a PR mesclado.

## Auditoria de arquitetura/deploy
Em Auditoria Extrema, leia e execute também `docs/quality/ARCHITECTURE_DEPLOY_AUDIT_V1.md`. Avalie caminho crítico de CI/deploy, runners, build/artifact, cache, provisionamento/restarts, migrations, contratos cross-repo, ownership de dados, workflow sprawl, hotspots e rollback.

<!-- EXECUTION_PROVENANCE_POLICY_V1 -->
## Assinatura e origem obrigatorias de toda execucao

Antes de qualquer acao material, leia e cumpra EXECUTION-PROVENANCE-POLICY.md. Toda execucao automatizada ou operacional deve carregar identidade, origem e execution_id verificaveis; recursos temporarios devem ter owner/origin e cleanup. Use scripts/emit-execution-provenance.py como formato de referencia. Nunca registre secrets.


<!-- BROWSER_SESSION_POLICY_V1 -->
## Navegador: VM canônica e cleanup obrigatório
Para browser interativo/remoto, use a VM backend canônica e a sessão gráfica prevista pela política global; não pergunte por host nem faça fallback para Windows. Sessões transitórias devem ter ownership + TTL e cleanup ao final. Em Auditoria Extrema, headless-only nunca certifica E2E quando UI real está disponível. Leia `AUDIT_BROWSER_E2E_REAL_V1.md`.

<!-- GLOBAL_TASK_CONTINUITY_V8 -->
## Global task continuity V8
Tasks that can mutate code, infrastructure, data, CI, or deployment must use `python3 scripts/agent_task_state.py` to persist a durable checkpoint before substantive work and after material progress. This repository is pinned as `repository=Vivaliz-site/-shopvivaliz-pipeline`. Recoverable failures remain RUNNING; only fresh verification permits CONCLUIDO. The adapter fails closed if the canonical A1 controller is unavailable. Detached recovery does not reopen the same ChatGPT conversation. Background recovery remains Gemini-only; Codex is never an automatic fallback and remains the last explicit option.
<!-- /GLOBAL_TASK_CONTINUITY_V8 -->

<!-- CHECKPOINT_FIRST_V9 -->
## Checkpoint antes da primeira etapa material
Toda tarefa potencialmente longa ou mutável deve registrar `agent_task_state.py start`
**antes** da primeira investigação extensa, chamada remota material, edição, mutação,
execução longa, delegação ou espera de CI. O objetivo é eliminar a janela em que uma
interrupção do ChatGPT ocorre antes de existir estado durável.

Depois de cada avanço material, atualize `progress` com evidência e `next_action`.
Não adie o primeiro checkpoint para depois do diagnóstico. Se o contexto atual não
consegue alcançar o controlador canônico, falhe fechado para tarefas que dependem de
retomada automática e use a rota operacional auditável que consiga registrar o estado.
<!-- /CHECKPOINT_FIRST_V9 -->

