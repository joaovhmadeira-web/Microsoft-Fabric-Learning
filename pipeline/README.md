# pipeline — orquestração Fabric (Dia 2)

Orquestração do fluxo Medallion **Bronze → Silver → Gold** via **Data Pipeline** do Fabric.

## Pipeline: `pl_olist_medallion`

Duas *Notebook activities* encadeadas por **On success**:

```
[nb_bronze_to_silver] ──(success)──► [nb_silver_to_gold]
```

| Atividade | Notebook | Papel |
|---|---|---|
| `nb_bronze_to_silver` | `bronze_to_silver` | Limpa/tipa Bronze → grava `slv_*` (Delta) |
| `nb_silver_to_gold`   | `silver_to_gold`   | Modela estrela → grava `gold_dim_*`/`gold_fact_*` (Delta + OPTIMIZE/V-Order) |

- **On success** (seta verde): o Gold só roda se o Silver concluir sem erro.
- Notebooks são **idempotentes** (`overwrite`) → o pipeline pode rerodar sem duplicar dados.
- **Validado** e **executado** com sucesso ponta a ponta (as duas atividades verdes).

## Agendamento

- **Configurado:** diário às **03:00** (janela de baixa demanda — libera a capacity no horário comercial).
- Pelo escopo do projeto, basta **existir configurado** (não precisa disparar em produção).

## Versionamento / Git do Fabric

**Status: adiado — bloqueado por política do tenant.**

- A integração **Git do Fabric com GitHub não está disponível** no tenant corporativo atual (restrição de organização). Numa migração real, "qual provider de Git o tenant permite" é uma restrição de governança levantada no planejamento — registrada aqui como tal.
- **Alternativa quando liberado:** **Azure DevOps Repos** é o provider de Git do Fabric mais comumente permitido em tenant corporativo. Fluxo: Workspace settings → Git integration → Azure DevOps → repo/branch + subpasta dedicada (ex.: `/fabric-workspace`) para isolar os itens serializados pelo Fabric da estrutura curada do repo.
- **Plano B em uso:** os artefatos (notebooks `.ipynb` + esta definição de pipeline) são versionados manualmente neste repositório Git.

## A versionar aqui (prints)

- [ ] Print do canvas do pipeline (duas atividades ligadas pela seta verde)
- [ ] Print da execução bem-sucedida (atividades verdes)
- [ ] Print da tela de agendamento (Schedule)
