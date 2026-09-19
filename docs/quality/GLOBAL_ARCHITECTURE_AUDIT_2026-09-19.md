# Auditoria Global de Arquitetura, Código e Deploy — 2026-09-19

## Escopo
Organização `Vivaliz-site`, seis repositórios ativos:
- `site-shopvivaliz`
- `-shopvivaliz-pipeline`
- `amazon-returns-safet`
- `ml-pricing-api`
- `mercadolivre-returns-recovery`
- `shopvivaliz-m365`

Método: `AUDIT_POLICY.md` versão `2026-09-19-universal-architecture-v5`, Runtime Parity, Universal Coverage e `ARCHITECTURE_DEPLOY_AUDIT_V1`.

## Resumo executivo

| Projeto | Arquivos | Workflows | Testes observados | Principal hotspot | Estado arquitetural |
|---|---:|---:|---:|---|---|
| site-shopvivaliz | 4726 | 351 | 429 | `master-production-pipeline.yml` + PHP monolítico | melhorias aplicadas; redução de workflow sprawl ainda necessária |
| -shopvivaliz-pipeline | 46 | 3 | 1 | `git_autonomous_agent.py` (659 linhas) | governança global consolidada; ampliar testes |
| amazon-returns-safet | 632 | 5 | 361 | Seller Central bridge (1520 linhas), daemon (1023) | CI forte; separar provisionamento de release |
| ml-pricing-api | 219 | 2 | 48 | pricing/listing/order | segurança de env em remediação; falta deploy imutável/proveniência |
| mercadolivre-returns-recovery | 250 | 3 | 80 | production ops (553), projection repo (408) | CI rápido; mover Composer do cutover para artifact |
| shopvivaliz-m365 | 56 | 3 | 0 no início | automation (343), Exchange client (275) | testes e deploy hardening aplicados nesta auditoria |

> Contagem de testes é baseada no inventário por caminhos/nomes rastreados na coleta; para M365 o snapshot inicial tinha zero. A auditoria adicionou uma suíte unitária posteriormente.

## Evidência de performance de CI
Amostras recentes antes/durante a auditoria:
- site `Quality Gate`: aproximadamente 308–566 s em PRs observados; o principal problema era também fila no runner de produção.
- Amazon Returns CI: aproximadamente 34–56 s.
- ML Pricing CI: aproximadamente 63–115 s.
- ML Returns CI: aproximadamente 38–76 s.
- M365 Governance CI: aproximadamente 9–21 s antes da nova suíte unitária.

## Correções executadas

### 1. Governança global
**CORRIGIDO**
- Política global v5 criada.
- Manifesto canônico de hashes criado em `docs/quality/GLOBAL_AUDIT_MANIFEST.json`.
- Validador cross-repo fail-closed criado.
- `CLAUDE.md` e `AGENTS.md` vinculados ao protocolo global.
- Self-test da própria auditoria ampliado para arquitetura/deploy.
- Pipeline global corrigido para usar o repositório canônico `Vivaliz-site/site-shopvivaliz`.
- Cache pip habilitado no pipeline global.

### 2. site-shopvivaliz
**CORRIGIDO**
- `Quality Gate` de CI puro removido do runner `shopvivaliz-a1-deploy` e movido para `ubuntu-latest`.
- Main validada com `AUDIT_GOVERNANCE_SELF_TEST=PASS` e `GLOBAL_AUDIT_POLICY=PASS`.

**FINDINGS**
- Snapshot pré-v5 de `.github/workflows`: 349 arquivos, sendo 221 `.yml` ativos e 128 desativados; após artefatos novos, 351 arquivos rastreados na pasta.
- Hotspots first-party grandes: `index.php` 1253 linhas, `produto.php` 1134, `checkout.php` 1087, `includes/tiny-order-push.php` 1046, `checkout-v2/index.php` 1004, `api/liz-intelligent.php` 950.
- `master-production-pipeline.yml` foi o arquivo mais alterado entre os últimos 80 commits observados.

**IMPROVEMENT_REQUIRED**
- Arquivar one-shots e workflows desativados fora da superfície executável.
- Consolidar workflows equivalentes em reusable workflows.
- Decompor checkout/index/produto e Tiny/Liz por domínio/adapters, preservando contratos e testes.

### 3. Amazon Returns / SAFE-T
**CORRIGIDO**
- Governança global v5 sincronizada.
- Audit Governance e Amazon Returns CI verdes no HEAD posterior à integração.

**FINDINGS**
- Seller Central bridge: 1520 linhas.
- daemon: 1023 linhas.
- `CaseRepository`: 697 linhas.
- `TenantOutbox`: 646 linhas.
- `SafeTDecisionEngine`: 627 linhas.
- `ErpSalesReturnTask.php` foi o maior hotspot de churn observado.
- `provision-production.sh` reúne release, migrations, Apache, systemd, certificados, browsers, timers e canaries.

**IMPROVEMENT_REQUIRED**
- Separar `build/release`, `infra drift/provision`, `migration`, `activate` e `post-deploy reconcile`.
- Provisionar Apache/systemd/certbot/browser somente quando input/hash/drift relevante mudar.
- Decompor bridge/daemon preservando state machine e idempotência.

### 4. ML Pricing API
**CORRIGIDO / EM VALIDAÇÃO**
- Arquivos `.env` reais removidos do HEAD do branch de remediação.
- Exemplos sanitizados criados.
- CI passa a rejeitar env real rastreado.
- Validador dos templates alterado para usar somente exemplos sanitizados.
- Composer cache adicionado.
- Symfony recebe `.env` somente de forma efêmera no workspace de CI.

**SECURITY FINDING**
O snapshot inicial possuía campos sensíveis não-placeholder em `.env.test`, inclusive segredo de cliente e chave de criptografia. Nenhum valor foi reproduzido neste relatório.

**IMPROVEMENT_REQUIRED**
- Após merge da remoção, avaliar rotação das credenciais potencialmente expostas.
- Limpeza retroativa do histórico só com plano/backup, pois reescrever histórico é destrutivo.
- Há units systemd no repositório, mas não foi encontrado caminho de deploy imutável/proveniência comparável ao site/SAFE-T.
- Criar `commit → artifact → release → current → health/version` antes de considerar produção plenamente reproduzível.

### 5. Mercado Livre Returns Recovery
**CORRIGIDO**
- Governança v5 integrada.
- Composer cache no CI.
- CI e Audit Governance verdes após merge.

**FINDINGS**
- `mlrr-production-ops.sh`: 553 linhas.
- `ReturnProjectionRepository.php`: 408 linhas.
- `ReturnProjectionNormalizer.php`: 334 linhas.
- `ClaimsRangeReconciler.php`: 301 linhas.
- Deploy produtivo executa `composer install --no-dev` dentro do release no host durante a operação.

**IMPROVEMENT_REQUIRED**
- Gerar artifact com `vendor/` em CI e promover o mesmo artifact/digest para produção.
- Reduzir tempo de cutover e dependência de rede/Packagist no host.
- Separar prepare/deploy/cutover/validate em componentes menores testáveis, preservando o fail-closed atual.

### 6. M365
**CORRIGIDO**
- Deploy deixou de executar `automation.py` como “teste” durante instalação; deploy não produz mais efeito externo só para validar código.
- URL placeholder substituída pelo repositório canônico.
- `set -Eeuo pipefail`.
- venv/dependências só são reinstalados quando `requirements.txt` muda.
- CI valida sintaxe do script de deploy.
- Bug de precedência encontrado: documentação dizia `environment > YAML > env_file`, mas YAML sobrescrevia environment.
- Loader corrigido e coberto por teste.
- Testes sem rede adicionados para configuração, auth/cache MSAL e Graph.
- Governance CI com pip cache + pytest ficou verde.

**IMPROVEMENT_REQUIRED**
- Migrar de `git pull` mutável em `/opt/m365` para releases imutáveis + `current` symlink.
- Adicionar testes do `ExchangeOnlinePowerShellClient` com subprocess mockado.
- Separar requirements de runtime e dev/test e gerar lock reproduzível.

## Riscos cross-repo

### P1 arquitetural — host de produção compartilhado
Site, ML Returns e outras operações usam o mesmo host/runner em partes do ciclo. GitHub `concurrency` é repo-scoped e não protege operações de repositórios diferentes.

**Ação recomendada:** lock no host, por exemplo uma primitiva única de `flock` para deploy/provision/cutover que compartilhem `shopvivaliz-free-a1`. Deve ser projetado com timeout, owner e recuperação de lock; não aplicar às cegas em produção.

### P1 arquitetural — contratos cross-repo implícitos
ML Returns e outros componentes leem artefatos/estado sob `/home/ubuntu/shopvivaliz-deploy/shared/...`.

**Ação recomendada:** versionar contratos de arquivo/API, adicionar contract tests produtor↔consumidor e owner canônico. Acesso a internals de outro repo sem contrato é dívida.

### P2 — workflow sprawl
O site concentra centenas de arquivos na pasta de workflows, elevando custo cognitivo, risco de trigger duplicado e diagnóstico.

**Ação recomendada:** inventário automático `active / scheduled / workflow_run / manual / disabled / one-shot`, deduplicação e budget de workflows.

### P2 — build no host de produção
ML Returns e M365 ainda possuem dependência maior do host durante deploy; SAFE-T mistura provisionamento amplo com release.

**Ação recomendada:** build-once/promote, artifact checksum/digest, dependências resolvidas antes do cutover e provisioning apenas por drift.

## Próximas otimizações priorizadas

| Prioridade | Ação | Benefício esperado | Critério de conclusão |
|---|---|---|---|
| P1 | host-level production operation lock | evita deploy/cutover concorrente cross-repo | teste concorrente prova exclusão e timeout/recovery |
| P1 | ML Returns build-once artifact | cutover menor e menos dependência externa | produção usa artifact do SHA já testado |
| P1 | immutable deploy para ML Pricing | proveniência e rollback | endpoint/runtime prova SHA/digest e rollback ensaiado |
| P1 | immutable deploy para M365 | rollback/reprodutibilidade | release dirs + current + health + rollback |
| P1 | split SAFE-T provisioning vs release | menor blast radius e deploy mais rápido | deploy comum não reinstala infra sem drift |
| P2 | contracts cross-repo | reduz quebra por acoplamento implícito | producer/consumer contract CI |
| P2 | workflow consolidation no site | reduz fila/complexidade | inventário e budget; one-shots arquivados |
| P2 | decomposição de hotspots | manutenção/testabilidade | módulos menores com regressão equivalente |
| P2 | DORA/lead-time telemetry | melhora contínua mensurável | queue/build/deploy/rollback medidos por projeto |

## Conclusão
A maior melhoria imediata de velocidade foi **tirar CI puro do runner de produção do site**. Os CIs de SAFE-T e ML Returns já são relativamente rápidos; nesses projetos o próximo ganho está em reduzir trabalho no **cutover/provisionamento**, não em remover testes.

A arquitetura não deve ser considerada “finalizada” enquanto os P1 arquiteturais acima permanecerem sem implementação/prova. As correções SAFE desta rodada foram aplicadas; mudanças de cutover, locks cross-repo e reestruturação de releases exigem implementação dedicada com rollback e validação de runtime.
