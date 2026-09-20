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

Quando houver auditoria completa/extrema, validação de release/apto ou gatilho de `AUDIT_POLICY.md`, execute integralmente `AUDIT_POLICY.md`, `docs/quality/EXTREME_AUDIT_PROTOCOL.md`, `docs/quality/AUDIT_RUNTIME_PARITY_V1.md`, `docs/quality/AUDIT_UNIVERSAL_COVERAGE_V1.md`, `docs/quality/AUDIT_SELF_TEST_V1.md` quando aplicável e `docs/quality/AUDIT_OVERLAY.md`. Corrija achados SAFE, procure falhas silenciosas/órfãos/flaky/unknown unknowns e não encerre em relatório sem remediação.

## Auditoria de arquitetura/deploy
Em Auditoria Extrema, leia e execute também `docs/quality/ARCHITECTURE_DEPLOY_AUDIT_V1.md`. Avalie caminho crítico de CI/deploy, runners, build/artifact, cache, provisionamento/restarts, migrations, contratos cross-repo, ownership de dados, workflow sprawl, hotspots e rollback.

<!-- EXECUTION_PROVENANCE_POLICY_V1 -->
## Assinatura e origem obrigatorias de toda execucao

Antes de qualquer acao material, leia e cumpra EXECUTION-PROVENANCE-POLICY.md. Toda execucao automatizada ou operacional deve carregar identidade, origem e execution_id verificaveis; recursos temporarios devem ter owner/origin e cleanup. Use scripts/emit-execution-provenance.py como formato de referencia. Nunca registre secrets.


<!-- BROWSER_SESSION_POLICY_V1 -->
## Navegador: escolha de host e cleanup obrigatorio
Antes de browser interativo/remoto, se o host nao estiver explicitamente definido na tarefa, pergunte qual maquina usar. Sessoes invisiveis/headless transitorias devem ter ownership + TTL padrao de 2h renovavel por heartbeat e cleanup ao final/boot. Orfaos podem ser limpos antes; sessoes visiveis e bridges persistentes documentadas devem ser preservadas. Nunca matar navegador globalmente por nome de processo. Leia a politica completa em `REGRAS-AGENTES-CENTRALIZADAS.md` (BROWSER_SESSION_POLICY_V1).
