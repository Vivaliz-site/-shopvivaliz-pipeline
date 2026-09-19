# Estado da Auditoria

**Status:** NÃO APTO

Primeira auditoria formal registrada em 2026-09-16 segundo `EXTREME_AUDIT_PROTOCOL.md`, `AUDIT_RUNTIME_PARITY_V1.md`, a matriz de transições/dados históricos e o overlay do projeto.

## Última auditoria válida
- Data: 2026-09-16.
- Commit/SHA auditado: `31a9653d88437f19a499e5075991d12dde623ca8`.
- Ambiente: GitHub Actions / workflow `Pipeline`.
- Veredito: **NÃO APTO PARA EXECUÇÃO OPERACIONAL CERTIFICADA**.
- Confiança: muito alta.
- Stop-the-line: o pipeline funcional não é executado desde 2026-06-29 e o workflow atual tenta fazer checkout de um repositório que não existe no namespace configurado.

## Evidência fresca desta auditoria
- `Repository Governance Gate` no SHA auditado concluiu com sucesso.
- O workflow funcional `.github/workflows/pipeline.yml` é apenas `workflow_dispatch`; as duas últimas execuções observadas são de 2026-06-29, uma falha e uma posterior success, ambas em SHAs antigos.
- O workflow atual executa `actions/checkout` de `fredmourao-ai/Shopvivaliz-site` usando `GH_PAT`.
- A consulta atual ao GitHub para `fredmourao-ai/Shopvivaliz-site` retornou 404/Not Found.
- O projeto ativo/canônico auditado em paralelo é `Vivaliz-site/site-shopvivaliz`; portanto o checkout do pipeline está apontando para namespace/repositório divergente.
- Não foi disparado o workflow para evitar consumir IA e efeitos externos enquanto o preflight já prova que o contrato de checkout está inválido.

## Matriz de operação e paridade
| Operação | Cobertura/definição | Evidência runtime atual | Resultado |
| --- | --- | --- | --- |
| checkout do próprio pipeline | workflow definido | não executado no SHA atual | NÃO VALIDADO |
| checkout do site alvo | aponta `fredmourao-ai/Shopvivaliz-site` | repo retorna 404 | **FAIL** |
| instalação de dependências | definida | não executada no SHA atual | NÃO VALIDADO |
| processamento IA | `scripts/main.py` + limite de chamadas | última execução funcional em 2026-06-29 | STALE |
| geração de artefatos | upload definido | não demonstrado no SHA atual | NÃO VALIDADO |
| persistência/push de resultados | comentário promete read/write, mas workflow não mostra etapa explícita de push | efeito atual não comprovado | NÃO VALIDADO |
| rollback/retry/idempotência | não demonstrados pelo workflow observado | sem exercício recente | NÃO VALIDADO |

## Achados
### P1 — dependência de checkout aponta para repositório inexistente
**COMPROVADO.** O workflow referencia `fredmourao-ai/Shopvivaliz-site`; a API GitHub responde 404. No estado atual, uma execução nova não possui precondição comprovada para chegar ao processamento.

### P1 — ausência de execução produção-equivalente recente
O último `Pipeline` funcional observado é de 2026-06-29. Governance verde não valida dependências, secrets, quotas, artefatos ou efeitos do pipeline no SHA atual.

### P2 — contrato de escrita/efeito externo não é verificável no YAML observado
O comentário do checkout afirma acesso de leitura/escrita para push de resultados, mas não há etapa explícita de commit/push no workflow exibido. É necessário provar onde ocorre o efeito e sua idempotência/reconciliação.

### P2 — falta prova de retry/rollback e limites além do teto de AI calls
Há concorrência com `cancel-in-progress` e timeout, mas não há evidência runtime atual de recuperação parcial, retomada segura ou rollback de artefatos/resultados.

## Risco residual
Alto para uso operacional: o workflow canônico está desatualizado em relação ao repositório alvo e não possui execução atual que demonstre o caminho completo.

## Saída do NO-GO
1. corrigir o repositório alvo para a fonte canônica atual e adicionar preflight explícito;
2. executar o pipeline em dados/cópia controlada, com orçamento baixo de IA, sem alterar produção;
3. comprovar artefatos, persistência e idempotência/retry/rollback;
4. versionar evidência de cada efeito externo e executar reauditoria contraditória;
5. somente depois habilitar execução com efeitos de escrita.

## Regra de validade
Esta auditoria cobre o SHA `31a9653d88437f19a499e5075991d12dde623ca8` e o estado dos workflows observado em 2026-09-16. Qualquer correção do target, secrets, modelo de IA ou write path exige reauditoria.