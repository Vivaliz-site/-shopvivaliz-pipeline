<!-- EXTREME_AUDIT_UI_FIRST_HARD_GATE_V1 -->
> **AUDITORIA EXTREMA V5 = UI REAL OBRIGATORIA.** Antes de declarar `APTO` ou `CONCLUIDO`, o proprio agente percorre cada jornada material na interface grafica real (navegacao, cliques, preenchimento, resultado visivel, reload/revisita, persistencia e evidencia visual com ambiente/release). API, terminal, SQL, codigo, screenshot isolado, mocks e testes apenas headless nao substituem prova pela UI. A auditoria inclui investigacao, correcao e reauditoria visual apos reparo. Nao ocultar uma UI marcando `browser.required=false` ou `journey.ui=false`. Somente componentes comprovadamente sem UI podem usar excecao com inventario negativo documentado e evidencias. Em bloqueio de sessao, esgotar rotas autorizadas; nao burlar MFA/permissaos. Leia e obedeça a secao `EXTREME_AUDIT_UI_FIRST_HARD_GATE_V1` de `AGENTS.md` antes da tarefa.
<!-- /EXTREME_AUDIT_UI_FIRST_HARD_GATE_V1 -->

<!-- AUDIT_EXTERNAL_REMEDIATION_V1 -->
> **AUDITORIA EXTERNA:** também é corretiva. Se houver autorização de escrita, corrigir + testar + reauditar. Se o auditor for somente leitura/independente, o relatório não é estado terminal: encaminhar os achados a executor autorizado e manter a tarefa aberta até correção e revalidação independente ou bloqueio externo comprovado.
<!-- /AUDIT_EXTERNAL_REMEDIATION_V1 -->
<!-- AUDIT_REMEDIATE_VALIDATE_GLOBAL_V1 -->
> **AUDITORIA CORRETIVA OBRIGATÓRIA:** qualquer auditoria deve investigar causa raiz, corrigir achados materiais seguros/autorizados, prevenir recorrência quando pertinente, testar e reauditar. Não encerrar em relatório de erros. APTO/CONCLUIDO exige evidência fresca pós-correção/E2E aplicável. Fonte: `REGRAS-AGENTES-CENTRALIZADAS.md`.
<!-- /AUDIT_REMEDIATE_VALIDATE_GLOBAL_V1 -->

<!-- DIAGNOSTIC_REMEDIATE_VALIDATE_GLOBAL_V1 -->
> **DIAGNÓSTICO CORRETIVO GLOBAL:** diagnóstico confirmado obriga correção segura, prevenção pertinente, testes e validação real/E2E aplicável antes de `CONCLUIDO`. Enquanto houver ação executável, permaneça `RUNNING`; só `BLOCKED_EXTERNAL` comprovado permite encerrar sem corrigir.
<!-- /DIAGNOSTIC_REMEDIATE_VALIDATE_GLOBAL_V1 -->
<!-- CLAUDE_READ_AGENTS_FIRST_V1 -->
> **BOOTSTRAP OBRIGATORIO DO CLAUDE:** antes de analisar, planejar, editar, executar comandos, usar navegador, abrir PR, fazer merge, deploy ou validar qualquer tarefa, leia **integralmente** o `AGENTS.md` da raiz deste repositorio e cumpra todas as instrucoes vigentes nele. Releia o `AGENTS.md` em retomadas de conversa ou quando o arquivo mudar. Se houver divergencia entre este `CLAUDE.md` e o `AGENTS.md`, o `AGENTS.md` prevalece. Nao prossiga assumindo memoria de uma leitura antiga.

@AGENTS.md

<!-- GLOBAL_BROWSER_VM_POLICY_V2 -->
> **NAVEGAÇÃO GLOBAL — VM OBRIGATÓRIA; WINDOWS PROIBIDO PARA BROWSER:** qualquer navegador, automação browser, sessão gráfica, Playwright/Selenium/CDP, Chrome/Chromium/Edge/Opera, CAPTCHA, MFA, consentimento ou validação visual deve usar por padrão e obrigatoriamente a VM backend `always-free-arm-1787907847-26` (`10.0.1.38`) e o Browser Worker privado. Para intervenção humana, usar `https://shopvivaliz.com.br/admin/browser-worker.php`. **Fred-Win (`LAPTOP-NIG4IFUU`) e `DESKTOP-KOCEPSV` não são destinos nem fallback para navegação.** Não perguntar qual máquina usar para browser: use a VM. Exceção somente se o proprietário ordenar explicitamente, na tarefa atual, o uso de um Windows específico para aquela navegação. Se a VM estiver indisponível, reparar o caminho VM/OCI Bastion/túnel privado ou registrar bloqueio real; nunca migrar silenciosamente para Windows. Workflows/relays Windows de browser são legado e não devem ser executados até serem migrados. A regra não proíbe Windows para tarefas não-browser que realmente dependam dele.

<!-- audit-refs: AUDIT_POLICY.md docs/quality/EXTREME_AUDIT_PROTOCOL.md docs/quality/AUDIT_RUNTIME_PARITY_V1.md docs/quality/AUDIT_UNIVERSAL_COVERAGE_V1.md docs/quality/AUDIT_SELF_TEST_V1.md docs/quality/ARCHITECTURE_DEPLOY_AUDIT_V1.md docs/quality/AUDIT_BROWSER_E2E_REAL_V1.md docs/quality/AUDIT_JOURNEY_INVENTORY_V1.md docs/quality/AUDIT_CLEAN_ROOM_REALITY_V1.md docs/quality/AUDIT_HARDENING_MAX_V1.md docs/quality/AUDIT_APTO_REMEDIATION_LOOP_V1.md docs/quality/AUDIT_ESCAPE_INVALIDATION_V1.md docs/quality/AUDIT_ABSOLUTE_GATE_V1.md docs/quality/AUDIT_AUTH_CREDENTIAL_DISCOVERY_V1.md docs/quality/AUDIT_MERGE_ENFORCEMENT_V1.md docs/quality/AUDIT_PROJECT_REQUIREMENTS_V1.md -->
<!-- absolute-audit: ler também docs/quality/AUDIT_PROJECT_REQUIREMENTS.json; antes de bloqueio auth/login executar AUDIT_AUTH_CREDENTIAL_DISCOVERY_V1; executar também AUDIT_MERGE_ENFORCEMENT_V1 e o Main Guard; somente scripts/certify-audit-manifest.py AUDIT_VERDICT=APTO autoriza declarar APTO; corrigir bloqueadores até lá -->
<!-- gate: FINAL_RESPONSE_DEPLOY_GATE_V1 — resposta final só após validação pós-deploy completa -->

<!-- EXECUTION_PROVENANCE_POLICY_V1 -->
@EXECUTION-PROVENANCE-POLICY.md


<!-- BROWSER_SESSION_POLICY_V1 -->
Leia e cumpra AGENTS.md e a secao BROWSER_SESSION_POLICY_V1 de REGRAS-AGENTES-CENTRALIZADAS.md antes de qualquer uso de navegador.
