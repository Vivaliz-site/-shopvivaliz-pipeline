# Acesso remoto canônico dos agentes — topologia atual (2026-10-29)

**Obrigatório:** antes de qualquer tarefa de VM, runtime, navegador, serviço, deploy, logs ou recuperação, ler no `main` de `Vivaliz-site/site-shopvivaliz` os arquivos `AGENTS.md`, `docs/knowledge/current-topology-and-access-2026-10-29.md`, `docs/knowledge/host-access.md` e `docs/knowledge/agent-rules.md`. Registrar SHA, host, identidade, sessão, permissão e evidência; documentos históricos desta pipeline não substituem o estado de runtime.

## Hosts válidos

| Destino | Conta OCI e função | Transporte operacional |
|---|---|---|
| `marina-a1-4c24g` | ESPOSA; **web/deploy/MySQL/workers/runner** | **Remote Desktop Commander direto** comprovado online; descobrir `deviceId` em `list_devices` e verificar `hostname -s`, `id -un` e autorização; RDC 2 e SSH privado/Tailscale exigem provas próprias |
| `always-free-arm-1787907847-26` | PRINCIPAL; backend/controller/MCP central/browser corporativo/MEI/M365 | **ShopVivaliz Remote Control MCP**, limitado à allowlist válida, com `hosts_list` e `host_health` |
| `Fred-Win`, `KOCEPSV` | Suporte/estação Windows | Canal autorizado por host, confirmado antes do uso; nunca servidor web ou navegador canônico de agentes |

**VM antiga excluída:** `shopvivaliz-free-a1` (IP histórico `10.0.1.112`) foi excluída conforme confirmação do proprietário em 2026-10-29. Nunca acessar, testar, reiniciar, implantar ou recriar. Não redirecionar aliases antigos para Marina, não migrar comandos por simples troca de IP e não tratar histórico de quatro hosts como inventário atual.

## MCPs, SSH, GUI e Cloudflare

1. **Backend:** MCP central disponível, mas o catálogo `hosts_list` ainda inclui a VM excluída e **não contém Marina**. Esta divergência exige correção no código/serviço da controladora; não executar comandos contra a origem.
2. **Marina:** RDC direto é a rota atualmente comprovada para operações autorizadas. O `marina-direct-mcp` está apenas em staging/read-only; serviços locais e túnel independente `shopvivaliz-marina-mcp.service`/`shopvivaliz-marina-mcp-tunnel.service` estavam inativos. `shopvivaliz-cloudflared-admin.service` ativo não comprova acesso pelo MCP OpenAI. Não alegar sudo, shell remoto ou conector ChatGPT ativo sem prova efetiva.
3. **SSH privado/VCN/Tailscale:** somente se a identidade e a host key forem verificadas e o mecanismo realmente provisionado. Não usar SSH público, login root público, `StrictHostKeyChecking=no`, senha copiada ou chave herdada da VM origem.
4. **GUI e navegador:** browser/CDP de agentes ShopVivaliz permanece nos perfis corporativos isolados do backend quando autenticação e bridge forem comprovadas; RustDesk e desktop são canais gráficos com identidade e lease próprios. Windows não é fallback automático de browser de agente.
5. **GitHub Actions, OCI Bastion, console e Run Command:** somente bootstrap/recovery e operações formalmente habilitadas. Nunca contornar negativa explícita de privilégio, RBAC, MFA, lease ou aprovação por outro canal.

## Regras de execução

- Validar host, usuário, privilégio, diretório do repositório, SHA/branch, estado de release e ownership antes de mutação.
- Releases de produção são imutáveis; não editar `/home/ubuntu/shopvivaliz-deploy/current` nem a release ativa.
- Segredos, cookies, chaves, OTPs e tokens não entram em Git, logs, chat, comandos, screenshots ou arquivos compartilhados.
- Aplicar investigação, correção, prevenção, testes e validação no runtime/E2E; para interface, Auditoria Extrema V5 exige navegação real e evidências, não apenas shell/API.
- Se um canal falhar, verificar as alternativas **realmente provisionadas e autorizadas**, sem declarar bloqueio por uma falha isolada e sem loops/bypass.

## Fontes e estado

- [Topologia e MCPs atuais](https://github.com/Vivaliz-site/site-shopvivaliz/blob/main/docs/knowledge/current-topology-and-access-2026-10-29.md)
- [Acesso a hosts](https://github.com/Vivaliz-site/site-shopvivaliz/blob/main/docs/knowledge/host-access.md)
- [Regras dos agentes](https://github.com/Vivaliz-site/site-shopvivaliz/blob/main/docs/knowledge/agent-rules.md)
- [Auditoria de divergências documentais](https://github.com/Vivaliz-site/site-shopvivaliz/blob/main/docs/audits/2026-10-29-agent-documentation-consistency.md)

Conectores e credenciais só devem ser considerados ativos após teste real. Se esta pipeline divergir de uma evidência fresca/canônica do site, corrigir a pipeline; não perpetuar a arquitetura anterior.
