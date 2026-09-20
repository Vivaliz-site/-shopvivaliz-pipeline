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
