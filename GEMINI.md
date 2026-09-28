<!-- SHOPVIVALIZ_HOST_ACCESS_CANONICAL_V2 -->
## Acesso canônico aos hosts ShopVivaliz

Antes de qualquer operação em host, VM, runtime, navegador, serviço, deploy, logs ou recuperação, leia `docs/HOST-ACCESS.md`. No repositório principal, a fonte central detalhada permanece `Vivaliz-site/site-shopvivaliz:docs/knowledge/host-access.md`.

Regras obrigatórias:
- produção web/deploy: `shopvivaliz-free-a1`, privado `10.0.1.112`;
- backend/controller/browser: `always-free-arm-1787907847-26`, privado `10.0.1.38`;
- navegador de agente roda somente no backend/controller; não usar navegador operacional em Fred-Win ou KOCEPSV;
- shell Linux: preferir SSH privado/Tailscale com identidade dedicada; SSH público, senha interativa e root público são proibidos;
- sem rota privada: OCI Bastion/control plane auditável é bootstrap/recovery; RustDesk self-hosted é GUI; Desktop Commander é apenas contingência;
- Windows via backend: Fred-Win = `127.0.0.1:2222`; KOCEPSV = `127.0.0.1:2223`; os relays legados `5557/5558` são apenas bootstrap/recovery;
- evidência fresca obrigatória antes de operar: `hostname`, identidade (`whoami`/`id`), diretório e estado Git quando aplicável;
- nunca registrar em Git, docs, logs ou chat o conteúdo de chaves, senhas, tokens, cookies, OTP/TOTP ou secrets.
<!-- /SHOPVIVALIZ_HOST_ACCESS_CANONICAL_V2 -->

<!-- GEMINI_READ_AGENTS_FIRST_V1 -->
> **BOOTSTRAP OBRIGATÓRIO DO GEMINI:** antes de analisar, planejar, editar, executar comandos, usar navegador, abrir PR, fazer merge, deploy ou validar qualquer tarefa, leia integralmente o `AGENTS.md` da raiz deste repositório e siga suas regras. Releia em retomadas ou quando o arquivo mudar. Em conflito, `AGENTS.md` prevalece.

# Protocolo IA-to-CLI obrigatório

<!-- GLOBAL_BROWSER_VM_POLICY_V2 -->
> **NAVEGAÇÃO GLOBAL — VM OBRIGATÓRIA; WINDOWS PROIBIDO PARA BROWSER:** qualquer navegador, automação browser, sessão gráfica, Playwright/Selenium/CDP, Chrome/Chromium/Edge/Opera, CAPTCHA, MFA, consentimento ou validação visual deve usar por padrão e obrigatoriamente a VM backend `always-free-arm-1787907847-26` (`10.0.1.38`) e o Browser Worker privado. Para intervenção humana, usar `https://shopvivaliz.com.br/admin/browser-worker.php`. **Fred-Win (`LAPTOP-NIG4IFUU`) e `DESKTOP-KOCEPSV` não são destinos nem fallback para navegação.** Não perguntar qual máquina usar para browser: use a VM. Exceção somente se o proprietário ordenar explicitamente, na tarefa atual, o uso de um Windows específico para aquela navegação. Se a VM estiver indisponível, reparar o caminho VM/OCI Bastion/túnel privado ou registrar bloqueio real; nunca migrar silenciosamente para Windows. Workflows/relays Windows de browser são legado e não devem ser executados até serem migrados. A regra não proíbe Windows para tarefas não-browser que realmente dependam dele.


Antes de qualquer alteração, carregue e siga integralmente o protocolo canônico:

@./AI-TO-CLI-PROTOCOL.md

Ele complementa as regras específicas do projeto. Nenhuma alteração válida da tarefa pode ser abandonada sem merge validado na branch de destino.

<!-- EXECUTION_PROVENANCE_POLICY_V1 -->
Leia e cumpra EXECUTION-PROVENANCE-POLICY.md antes de qualquer execucao material.
