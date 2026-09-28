# Acesso canônico aos hosts ShopVivaliz

Este arquivo é um runbook local e **não contém segredos**. A fonte central detalhada é `Vivaliz-site/site-shopvivaliz/docs/knowledge/host-access.md`.

## Mapa operacional
- `shopvivaliz-free-a1` — produção web/deploy — privado `10.0.1.112`.
- `always-free-arm-1787907847-26` — backend/controller/browser — privado `10.0.1.38`.
- Fred-Win / `LAPTOP-NIG4IFUU` — reverse SSH no backend `127.0.0.1:2222`.
- KOCEPSV / `DESKTOP-KOCEPSV` — reverse SSH no backend `127.0.0.1:2223`.

## Estado conhecido em 2026-09-28
- Linux controller + target de produção: bootstrap comprovado.
- Fred-Win `2222`: PASS recente.
- KOCEPSV `2223`: rota canônica, **ainda não comprovada operacionalmente**; tratar como indisponível até validação fresca.

## Regras
- Navegador de agente somente no backend `always-free-arm-1787907847-26`; nunca em Fred-Win/KOCEPSV.
- Shell Linux: SSH privado/Tailscale com identidade dedicada. SSH público, senha interativa e root público são proibidos.
- Sem rota privada: OCI Bastion/control plane auditável para bootstrap/recovery. RustDesk self-hosted para GUI. Desktop Commander apenas contingência.
- Windows runtime: reverse SSH `2222/2223`; relays legados `5557/5558` apenas bootstrap/recovery.
- Antes de operar: provar `hostname`, `whoami`/`id`, `pwd` e estado Git quando aplicável.
- Produção é imutável: nunca editar `/home/ubuntu/shopvivaliz-deploy/current/` nem a release ativa.
- Remote Control MCP: controller `127.0.0.1:5580` no backend; endpoint nunca público; GitHub não é transporte/queue/heartbeat normal de runtime.
- Nunca registrar valores de chaves, senhas, tokens, cookies, OTP/TOTP ou secrets.
