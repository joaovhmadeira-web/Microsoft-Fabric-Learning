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

## Pendentes — Dia 3 (Direct Lake + Segurança)

- [ ] Modelo semântico Direct Lake sobre a Gold (diagrama estrela)
- [ ] Medidas DAX recriadas no modelo Direct Lake (paridade com o baseline do Dia 1)
- [ ] Regra RLS (vendedor × estado)
- [ ] Regra OLS (esconder `payment_value` do papel operacional)
- [ ] "View as role" mostrando o filtro aplicado

## Pendentes — Dia 4 (Capacidade, custos e negócio)

- [ ] Fabric Capacity Metrics após reprocessar o pipeline (consumo de CU)
- [ ] Comparativo antes/depois (legado vs. Fabric)
