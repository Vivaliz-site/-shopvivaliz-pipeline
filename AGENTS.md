<!-- GEPETO_EVERY_TASK_V1 -->
## Gepeto obrigatorio em toda tarefa
Acione o plugin Gepeto junto com Superpowers em toda tarefa e retomada, sem nova mencao do usuario. Leia e cumpra `GEPETO-POLICY.md`. Se o runtime nao expuser o plugin, registre `GEPETO_UNAVAILABLE`, informe a limitacao e continue o trabalho autorizado sem simular participacao. Aplicar um plugin nao comprova delegacao nem revisao independente.
<!-- /GEPETO_EVERY_TASK_V1 -->

<!-- AUDIT_UI_EVIDENCE_INTEGRITY_V2 -->
## GATE EXECUTAVEL — UI, evidencia real e continuidade da Auditoria Extrema V5

Antes de declarar APTO, executar `scripts/certify-audit-manifest.py` com `--evidence-root` e atender a `docs/quality/AUDIT_UI_EVIDENCE_INTEGRITY_V2.md`. A auditoria exige arquivos reais com hash recalculado, inventario de UI, log de passos/clicks e midia capturada, cada caso real stateful, RED/GREEN/regressao/reauditoria, reviewer em sessao independente e UI pos-deploy. E proibido autoatribuir APTO com flags, mock, screenshot isolado, API, CLI, SQL ou headless-only. Enquanto nao obtiver AUDIT_VERDICT=APTO da mesma release, preservar `RUNNING` no controlador de continuidade e `next_action` concreta, sem abandonar em relatorio, PR, merge, limite de turno ou falha recuperavel. Delegacao nao isenta o controlador. Antes de `CONCLUIDO`, validar E2E real e o gate `agent_task_state.py terminal`. Respeitar leases/fencing, MFA, aprovacao de destruicao/cobranca e proibir loops autonomos de IA paga. Bloqueio externo comprovado nao equivale a APTO.
<!-- /AUDIT_UI_EVIDENCE_INTEGRITY_V2 -->

<!-- EXTREME_AUDIT_UI_FIRST_HARD_GATE_V1 -->
## GATE INEGOCIAVEL: Auditoria Extrema V5 executada pela UI real

**Ordem explicita do proprietario (2026-10-13), vinculante a GPT, Claude, Gemini, Codex, subagentes, orquestradores e revisores:** toda auditoria extrema/completa/V5/aptidao de sistema que tenha UI **DEVE ser executada pelo proprio agente atraves da interface grafica real**. O auditor nao pode substituir a UI por API, terminal, SQL, inspecao de codigo, logs, mocks, healthcheck, testes unitarios, Playwright exclusivamente headless nem screenshot estatico. Esses meios sao auxiliares para investigar/reconciliar, jamais prova suficiente do funcionamento que o usuario vivencia.

1. **UI primeiro, sem atalhos:** inventariar telas, jornadas, perfis, estados e casos reais; abrir a interface publicada no host/perfil autorizado; navegar, clicar, preencher, filtrar, salvar/submeter dentro das permissoes; observar resposta visual, erros e efeitos; recarregar, sair e voltar para provar persistencia. Para Amazon Seller Central, Mercado Livre e paineis externos, auditar os casos e transicoes acessiveis na UI oficial, um a um conforme escopo, sem declarar sucesso por API somente.
2. **Evidencia obrigatoria por jornada:** registrar ambiente/URL, SHA/release quando aplicavel, sessao autorizada sem segredos, timestamp, passos efetivamente executados, capturas/trace/video, estado antes/depois, erros de console/rede, reload/revisita e reconciliacao independente dos efeitos duraveis. Screenshot isolado, abertura de pagina, resposta HTTP 200 ou teste simulado nao certificam jornada.
3. **Auditoria inclui reparo:** ao encontrar falha corrigivel no escopo autorizado, investigar causa raiz, corrigir, prevenir recorrencia, executar testes e **repetir o mesmo fluxo pela UI real apos correcao/deploy**, com evidencia independente. Nao encerrar no diagnostico, em PR ou em teste apenas de backend.
4. **Gate fail-closed, sem falso APTO:** qualquer fluxo com UI nao percorrido e comprovado permanece `NAO_VALIDADO_UI` / `NAO_APTO`; e proibido declarar `APTO`, `CONCLUIDO`, 100% ou verde. `browser.required=false` ou `journey.ui=false` nao podem ser usados para ocultar UI existente. Se realmente nao existir interface para o componente auditado, registrar inventario negativo de UI, justificativa e evidencias; validar os caminhos reais nao visuais pertinentes. Ausencia/falha transitoria de browser exige reparo/fallback autorizado antes de `BLOCKED_EXTERNAL`.
5. **Seguranca:** usar browser/desktop/MCP/RDC nos hosts e perfis previstos nos runbooks, com ownership/leases, controles de autorizacao e MFA; preservar sessoes. A auditoria nao autoriza exclusao, faturamento real, modificacao irreversivel ou acesso a segredo. Quando a acao terminal nao puder ser realizada com seguranca, testar ate o limite seguro e registrar exatamente a cobertura pendente; nunca inventar sucesso.

Fonte complementar: `AUDIT_POLICY.md`, `docs/quality/AUDIT_BROWSER_E2E_REAL_V1.md` e `docs/quality/AUDIT_ABSOLUTE_GATE_V1.md` do repositorio governado. **Este gate prevalece sobre instrucoes mais brandas que permitam certificar por API ou parecer do agente.**
<!-- /EXTREME_AUDIT_UI_FIRST_HARD_GATE_V1 -->

<!-- REMOTE_ACCESS_EXHAUSTION_GATE_V1 -->
## Gate obrigatório: esgotar acesso remoto antes de declarar bloqueio
Em `Retome`, `Continue`, `Prossiga`, `Siga` ou qualquer tarefa remota, uma falha de MCP/RDC/SSH/rede/autenticacao isolada **não** encerra a execução. Ler AGENTS.md, runbooks locais e `Vivaliz-site/site-shopvivaliz/docs/knowledge/host-access.md` (main atual), comprovando fonte e revisao. Identificar host, identidade e permissoes efetivas.
**Verificar todas as rotas aplicaveis, existentes e autorizadas, na prioridade do runbook:** ShopVivaliz Remote Control MCP/controller; RDC e RDC 2 se disponiveis/autorizados; SSH privado/VCN/Tailscale/tunel/reverse SSH documentado; `desktop_*`/bridge/RustDesk para GUI; OCI Bastion, OCI Compute Run Command, serial console e GitHub Actions somente para bootstrap/recovery/reparo, nunca como transporte normal de runtime. Browser ShopVivaliz permanece na VM backend, sem migracao para Windows. Para cada rota, testar conectividade, identidade e capacidade real; corrigir falhas tecnicas autorizadas, recuperar servico/sessao e aplicar retry idempotente e limitado ou fallback.
Registrar checkpoint nao secreto `remote_access_attempts` por host: rota, objetivo, `PASS/FAILED/NOT_PROVISIONED/NOT_APPLICABLE`, evidencias, causa, reparos e alternativa seguinte. Nao apresentar rota nao provisionada como testada. Manter `RUNNING` enquanto houver acesso alternativo viavel. **`BLOCKED_EXTERNAL` apenas apos exaurir e documentar todos os caminhos tecnicamente viaveis, seguros e autorizados.** `AWAITING_APPROVAL` exige identificar aprovacao obrigatoria exata. Proibidos bypass de MFA/RBAC/branch protection, exibir credenciais, abrir SSH publico, alterar browser para Windows sem autorizacao expressa ou loops infinitos.
<!-- /REMOTE_ACCESS_EXHAUSTION_GATE_V1 -->

<!-- GLOBAL_RESUME_VERIFIED_RULES_V3 -->
## Retome obrigatorio: leitura comprovada e execucao ate validacao
- `Retome`, `Continue`, `Prossiga` e `Siga` isolados sao ordens de executar a ultima tarefa pendente, nunca somente relatar status.
- Antes de cada retomada ou mutacao, ler o AGENTS.md vigente e a base canonica em Vivaliz-site/site-shopvivaliz: docs/knowledge/atendimento-chatgpt-bootstrap.md, host-access.md, README.md, agent-rules.md e runbooks especificos. Registrar checkpoint nao secreto `rules_loaded` com paths, refs, SHAs e instante; citar sem ler nao vale. Se sem acesso, recuperar leitura antes de mutacoes.
- Recuperar ultimo checkpoint e executar: identificar causa raiz, corrigir, testar, prevenir, usar fallback autorizado, continuar, validar runtime/E2E, integrar PR e deploy quando aplicavel.
- Proibido encerrar por diagnostico, relatorio, timeout, erro transitorio, CI ou PR. Antes de declarar bloqueio, esgotar e documentar todas as alternativas razoaveis, seguras e autorizadas, sem loops infinitos nem bypass de MFA, CI, aprovacoes ou seguranca.
- Manter RUNNING enquanto houver acao segura viavel; CONCLUIDO apenas com evidencias; BLOCKED_EXTERNAL somente com impedimento externo comprovado e checkpoint recuperavel. Nao prometer persistencia sem controlador ativo.
<!-- /GLOBAL_RESUME_VERIFIED_RULES_V3 -->

<!-- AUTONOMOUS_RESUME_TO_VALIDATED_COMPLETION_V1 -->
## Regra obrigatoria: retomar e executar ate conclusao comprovada

- Em toda tarefa operacional, recuperar o ultimo estado e checkpoint confiavel antes de agir; nao repetir operacoes ja concluidas nem descartar trabalho existente.
- Agir autonomamente dentro das permissoes vigentes. Diagnostico, relatorio, PR aberto, tentativa de comando, timeout ou falha transitoria nao encerram a tarefa.
- Ciclo obrigatorio: **verificar estado -> executar -> identificar falhas -> investigar causa raiz -> corrigir -> prevenir recorrencia -> testar -> retomar -> validar**.
- Diante de erro de browser, MCP, RDC, API, CLI, rede, sessao, worker ou integracao, verificar se a acao anterior teve efeito, recuperar de forma idempotente e tentar alternativas tecnicamente viaveis, seguras e autorizadas.
- Usar checkpoints, logs e estado persistente quando existirem. Nunca alegar trabalho em segundo plano ou retomada automatica se nao houver controlador realmente configurado e ativo.
- Manter a tarefa `RUNNING` enquanto existir proxima acao segura e viavel no ambiente de execucao. Declarar `CONCLUIDO` apenas com evidencias frescas, testes pertinentes, regressao e validacao runtime/E2E quando aplicavel.
- Se houver bloqueio externo objetivo ou aprovacao obrigatoria pendente, registrar causa, evidencias, tentativas, checkpoint e acao exata para retomar; nao contornar protecoes de branch, autenticacao, MFA, politicas de seguranca ou controles de aprovacao.
- Respeitar regras especificas do repositorio, limites da sessao e escopo de autorizacao. Acao destrutiva ou irreversivel exige autorizacao adequada.
- A regra vale para agentes, subagentes, Codex, MCP/RDC, automacoes, debugging, auditorias, deploys e retomadas; a resposta final deve distinguir entrega comprovada de bloqueio documentado.

Fonte global da politica: `Vivaliz-site/site-shopvivaliz/REGRAS-AGENTES-CENTRALIZADAS.md`.
<!-- /AUTONOMOUS_RESUME_TO_VALIDATED_COMPLETION_V1 -->

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

<!-- DIAGNOSTIC_REMEDIATE_VALIDATE_GLOBAL_V1 -->
> **DIAGNÓSTICO É CORRETIVO EM QUALQUER TAREFA:** identificar a causa não conclui o trabalho. Todo agente/controlador deve continuar de defeito confirmado para **correção segura → prevenção pertinente → testes → validação real/E2E aplicável → revalidação**. Enquanto houver ação segura executável, o estado é `RUNNING`; `CONCLUIDO` exige evidência fresca pós-correção. Só `BLOCKED_EXTERNAL` comprovado, após esgotar alternativas autorizadas, permite encerrar sem corrigir.
<!-- /DIAGNOSTIC_REMEDIATE_VALIDATE_GLOBAL_V1 -->

<!-- SHOPVIVALIZ_REMOTE_ACCESS_V1 -->
## Acesso remoto obrigatório para agentes

Antes de qualquer operação em VM, runtime, navegador, serviço, deploy, logs ou recuperação, leia **`docs/AGENT-REMOTE-ACCESS.md`** e o inventário em `Vivaliz-site/site-shopvivaliz/docs/knowledge/current-topology-and-access-2026-10-29.md` no `main`. **A escolha do canal depende do destino:** backend `always-free-arm-1787907847-26` pelo MCP central (allowlist válida); produção `marina-a1-4c24g` pelo RDC direto atualmente comprovado; SSH privado/Tailscale apenas com autenticação e host key verificadas; OCI/GitHub/serial para recuperação formal. `shopvivaliz-free-a1` foi excluída, não deve receber comandos nem ser recriada. O MCP independente da Marina não está ativo. Navegador de agentes ShopVivaliz permanece na VM backend e exige perfil corporativo correto, nunca fallback silencioso em Windows.

# Instruções obrigatórias para agentes

<!-- GLOBAL_BROWSER_VM_POLICY_V2 -->
> **NAVEGAÇÃO GLOBAL — backend com conta isolada:** browser/UI de agentes, Playwright/Selenium/CDP, ChatGPT/OpenAI, consentimento e MFA operam na VM backend `always-free-arm-1787907847-26` quando a bridge/sessão esteja **comprovadamente ativa e autorizada**, conforme `docs/knowledge/browser-sessions.md` e `docs/knowledge/shopvivaliz-graphical-session-recovery.md` de `Vivaliz-site/site-shopvivaliz` no `main`. `Fred-Win` e `KOCEPSV` não substituem navegador de agente; podem oferecer apoio de GUI/SSH dentro do escopo próprio. A URL histórica `https://shopvivaliz.com.br/admin/browser-worker.php` não comprova, por si, identidade ou estado de sessão: validar a rota real antes de interagir, sem criar perfis/cookies duplicados. Auditoria V5 exige UI real e evidências.

<!-- GLOBAL_BROWSER_SESSION_PROFILE_V1 -->
> **PERFIS CHATGPT DEV E ATENDIMENTO NUNCA SE MISTURAM:** perfil backend `shopvivaliz-dev-chromium` (CDP 9559) pertence exclusivamente a `dev@shopvivaliz.com.br`; perfil `shopvivaliz-atendimento-chromium` (CDP 9556) pertence exclusivamente a `atendimento@shopvivaliz.com.br`. Para cada ação/retomada, identificar o perfil exato e validar a sessão pela identidade oficial, preservar Keyring/MFA e lease; não fazer logout, substituir sessão, copiar cookies ou usar um perfil para autenticar o outro. O perfil genérico histórico `ai-squad-chatgpt` **não** substitui estes bindings nem comprova login; só operar outro perfil se runbook atualizado e autorização por identidade real o permitirem. Não contornar CAPTCHA/MFA nem solicitar credenciais já provisionadas sem preflight oficial.

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

<!-- SHOPVIVALIZ_GRAPHICAL_SESSION_RECOVERY_V1 -->
## Gate obrigatorio para todos os agentes: GUI ShopVivaliz e contas ChatGPT

Antes de diagnosticar RustDesk, VM, autenticacao Dev/Atendimento ou classificar um login como perdido, **ler efetivamente no `main` de `Vivaliz-site/site-shopvivaliz`** o runbook `docs/knowledge/shopvivaliz-graphical-session-recovery.md`, junto de `AGENTS.md` e `docs/knowledge/browser-sessions.md`, registrando `rules_loaded` com SHAs. Esta regra aplica-se a ChatGPT, Claude, Gemini, Gepeto, subagentes e rotinas persistentes deste repositorio.

Fatos observados em 2026-10-11: a area XFCE/RustDesk `fredconsole/:0` foi recuperada e mostrou Chromium ChatGPT no workspace Vivaliz com Dev e Atendimento no seletor; a tela LightDM `lightdm/:1` e login do **Ubuntu**, nao login ChatGPT; os perfis corporativos independentes permanecem no usuario `fredrdp`, display `:99`, Dev CDP9559 e Atendimento CDP9556. **Ver conta no seletor nao prova autenticacao individual**: exigir identidade exata em `/api/auth/session` no respectivo perfil antes de marcar `AUTHENTICATED`/`CONCLUIDO`. Nao reutilizar cookies entre perfis, nao destruir sessoes, nao solicitar senha ja provisionada e nao redefinir o GNOME Keyring por tentativa. Usar somente senha existente + TOTP oficial conforme preferencia atual do proprietario, respeitando etapas do provedor, MFA, lease e aprovacoes. Preservar checkpointer e monitor; `RUNNING` ate progresso real.
<!-- /SHOPVIVALIZ_GRAPHICAL_SESSION_RECOVERY_V1 -->
