# prints — capturas de tela do projeto

Registro visual da execução no portal Fabric, para o relatório/portfólio.

## Capturados — Dias 1 e 2

| Arquivo | O que mostra | Camada / etapa |
|---|---|---|
| `homepage_workspace.png` | Workspace **Fabric Learning** com os itens do projeto | Visão geral |
| `brz_files.png` | CSVs brutos do Olist em `Files/` no Lakehouse `lh_olist` | Bronze (ingestão) |
| `tabelas_brz_slv_gold.png` | Explorer do Lakehouse com `brz_*`, `slv_*` e `gold_*` sob `dbo` | Medallion completo |
| `brz_to_slv_rows_count.png` | Notebook `bronze_to_silver` — contagem de linhas das Bronze | Silver (sanidade) |
| `brz_to_slv_gravando_slv.png` | Notebook `bronze_to_silver` — saída `gravado slv_*` | Silver (gravação) |
| `slv_to_gold_gravando_optimize.png` | Notebook `silver_to_gold` — `gravado gold_*` + OPTIMIZE/V-Order | Gold (gravação) |
| `pipeline_execucao.png` | Pipeline `pl_olist_medallion` — execução com atividades verdes | Orquestração (run) |
| `pipeline_agendamento.png` | Pipeline `pl_olist_medallion` — agendamento diário 03:00 | Orquestração (schedule) |

## Capturados — Dia 4

| Arquivo | O que mostra | Etapa |
|---|---|---|
| `capacity_metrics_trial_error.png` | Capacity Metrics App falhando na capacity trial (`Error obtaining data location`) | Limitação de ambiente (FinOps) |

## Opcionais — Dia 3/4 (execução validada por outros meios)

O Dia 3 foi validado no **DAX Studio** (impersonação XMLA) e o Dia 4 pelo **Monitoring Hub** — prints abaixo são bônus, não bloqueiam a entrega:

- [ ] Diagrama estrela do modelo Direct Lake
- [ ] DAX Studio: RLS `Vendedor_SP`/`Vendedor_Dinamico` retornando só SP
- [ ] DAX Studio: OLS quebrando `[Total Pagamentos]` no papel `Operacional`
- [ ] Monitoring Hub: durações do reprocessamento do pipeline (~4m24s)
