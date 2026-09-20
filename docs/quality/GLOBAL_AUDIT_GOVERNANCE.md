# Governança Global da Auditoria Extrema

Fonte canônica: `Vivaliz-site/site-shopvivaliz`.

Versão atual: `2026-09-19-universal-error-coverage-v4`.

Projetos cobertos:
- `site-shopvivaliz`
- `-shopvivaliz-pipeline`
- `amazon-returns-safet`
- `ml-pricing-api`
- `mercadolivre-returns-recovery`
- `shopvivaliz-m365`

O workflow `Global Audit Governance Fleet` compara os artefatos globais byte a byte com o repositório canônico e verifica os bootstraps `AGENTS.md`, `CLAUDE.md` e `GEMINI.md`, além da execução do self-test em CI.

Drift é falha de governança. Regras específicas de domínio permanecem no `AUDIT_OVERLAY.md` e podem divergir por projeto; o contrato mínimo do overlay continua obrigatório.

## Política global de navegador

O gate verifica o marcador `GLOBAL_BROWSER_VM_POLICY_V2` em `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` e `REGRAS-AGENTES-CENTRALIZADAS.md` nos seis repositórios `Vivaliz-site` e também em:

- `fredmourao-ai/solange-rolla-consultorio`
- `fredmourao-ai/solange-rolla`
- `fredmourao-ai/mei-mg-email`

A política torna `always-free-arm-1787907847-26` o host obrigatório para navegação/browser e proíbe Fred-Win/KOCEPSV como fallback. Drift desse marcador é falha de governança.
