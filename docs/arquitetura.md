# Arquitetura & decisões

## Visão geral (Medallion)

```
CSV Olist ──► Bronze (raw, Delta) ──► Silver (limpo, tipado, joins) ──► Gold (dim/fato) ──► Direct Lake ──► Relatório
             [Lakehouse/OneLake]      [Notebook PySpark]              [Notebook/Dataflow]   [modelo semântico]
```

## Decisão 1 — Lakehouse vs. Warehouse

**Escolha: Lakehouse.**

| Critério | Lakehouse | Warehouse |
|---|---|---|
| Ingestão de arquivos brutos (CSV) | Nativo (Files + Tables) | Precisa de staging |
| Transformação | Spark/Notebooks + SQL | T-SQL |
| Direct Lake sobre Delta | Sim | Sim |
| Perfil da equipe | Engenharia de dados (PySpark) | BI/analista (T-SQL) |

Para este cenário (ingestão de CSV → transformação PySpark → Direct Lake), o Lakehouse cobre tudo sem mover dados entre itens. O Warehouse entraria se o time fosse majoritariamente T-SQL ou houvesse necessidade de transações multi-tabela ACID no modelo de escrita.

## Decisão 2 — Formato de arquivos

- **Bronze:** manter o CSV original como `Files/` + tabela Delta espelho (rastreabilidade da origem).
- **Silver/Gold:** **Delta Parquet** (padrão do Fabric, requisito do Direct Lake).

## Decisão 3 — Particionamento

- Volume do Olist é pequeno (~100k pedidos) → **não particionar** Silver/Gold prematuramente (evita _small files problem_).
- Se produção: particionar o fato `orders` por `year(order_purchase_timestamp)`.
- Rodar `OPTIMIZE` / `V-Order` na Gold para leitura Direct Lake eficiente.

## Decisão 4 — Modelo dimensional (Gold)

Esquema estrela:

- **Fatos:** `fact_orders` (grão: pedido), `fact_order_items` (grão: item do pedido).
- **Dimensões conformadas:** `dim_customer`, `dim_seller`, `dim_product`, `dim_date`.
- `order_payments` agregado por pedido e anexado ao `fact_orders` (coluna sensível → OLS no Dia 3).

## Convenções de nomenclatura

- Lakehouse: `lh_olist`
- Tabelas: prefixo por camada quando no mesmo Lakehouse (`brz_`, `slv_`, `gold_`) OU Lakehouses separados por camada. **Decisão:** um Lakehouse, prefixos por camada (menos overhead no trial).

## A preencher durante execução

- [ ] Print da estrutura do Lakehouse (Files + Tables)
- [ ] SKU da capacity trial usada
- [ ] Tempo de ingestão Bronze
