# Medidas DAX (antes/depois)

As mesmas medidas de negócio são implementadas no modelo **legado (import mode, Dia 1)** e recriadas no **Direct Lake (Dia 3)**. A lógica DAX é idêntica — o que muda é o modo de armazenamento por trás.

Grão dos fatos:
- `fact_order_items` — 1 linha por item de pedido (tem `price`, `freight_value`).
- `fact_orders` — 1 linha por pedido (tem timestamps de compra/entrega e `payment_value` agregado).

## 1. Receita total

Soma do valor dos itens vendidos.

```DAX
Receita Total = SUMX ( fact_order_items, fact_order_items[price] )
```

## 2. Receita por período

Basta cruzar `Receita Total` com `dim_date` (por `order_purchase_timestamp`). Variante YTD:

```DAX
Receita YTD =
    TOTALYTD ( [Receita Total], dim_date[date] )
```

## 3. Ticket médio

Receita dividida pela quantidade de pedidos distintos.

```DAX
Ticket Medio =
    DIVIDE (
        [Receita Total],
        DISTINCTCOUNT ( fact_orders[order_id] )
    )
```

## 4. % frete sobre o valor da venda

```DAX
Frete Total = SUMX ( fact_order_items, fact_order_items[freight_value] )

Pct Frete s/ Venda =
    DIVIDE ( [Frete Total], [Receita Total] )
```

## 5. SLA de entrega (prazo real vs. promessa)

Diferença, em dias, entre a data de entrega prometida e a real. Positivo = entregue antes do prometido.

```DAX
Dias vs Promessa =
    AVERAGEX (
        FILTER (
            fact_orders,
            NOT ISBLANK ( fact_orders[order_delivered_customer_date] )
                && NOT ISBLANK ( fact_orders[order_estimated_delivery_date] )
        ),
        DATEDIFF (
            fact_orders[order_delivered_customer_date],
            fact_orders[order_estimated_delivery_date],
            DAY
        )
    )

-- % de pedidos entregues no prazo
Pct No Prazo =
    VAR Entregues =
        CALCULATE (
            DISTINCTCOUNT ( fact_orders[order_id] ),
            NOT ISBLANK ( fact_orders[order_delivered_customer_date] )
        )
    VAR NoPrazo =
        CALCULATE (
            DISTINCTCOUNT ( fact_orders[order_id] ),
            fact_orders[order_delivered_customer_date]
                <= fact_orders[order_estimated_delivery_date]
        )
    RETURN DIVIDE ( NoPrazo, Entregues )
```

## Nota antes/depois

| Aspecto | Import mode (Dia 1) | Direct Lake (Dia 3) |
|---|---|---|
| Onde os dados vivem | Copiados no dataset (VertiPaq) | Lidos direto do Delta (Gold) |
| DAX das medidas | Idêntico | Idêntico |
| Refresh | Necessário (agendado) | Não copia dados (framing) |
| Observação | Baseline "antes" | Alvo da migração |

> `payment_value` é o eixo de OLS: a medida `Receita Total` acima usa `price` (itens), não `payment_value`. Se alguma medida usar `payment_value`, ela também fica restrita ao papel `Operacional`.

---

## Versão legado (Dia 1 — .pbix import mode)

Mesmas medidas, escritas para as tabelas do **modelo legado**: `orders` e `order_items` (sem prefixo `fact_`/`dim_` e sem `dim_date`). Copie e cole direto no Power BI Desktop.

> **Datas:** o modelo legado não tem `dim_date`. Para receita por período, deixe o **Auto date/time** do Power BI ligado e use a hierarquia de `orders[order_purchase_timestamp]`; ou crie uma coluna `Data = DATE(YEAR(...), MONTH(...), DAY(...))`. O `TOTALYTD` abaixo aponta direto para a coluna de timestamp.

```DAX
Receita Total = SUMX ( order_items, order_items[price] )

Frete Total = SUMX ( order_items, order_items[freight_value] )

Pct Frete s/ Venda = DIVIDE ( [Frete Total], [Receita Total] )

Ticket Medio =
    DIVIDE (
        [Receita Total],
        DISTINCTCOUNT ( orders[order_id] )
    )

Receita YTD =
    TOTALYTD ( [Receita Total], orders[order_purchase_timestamp] )

Dias vs Promessa =
    AVERAGEX (
        FILTER (
            orders,
            NOT ISBLANK ( orders[order_delivered_customer_date] )
                && NOT ISBLANK ( orders[order_estimated_delivery_date] )
        ),
        DATEDIFF (
            orders[order_delivered_customer_date],
            orders[order_estimated_delivery_date],
            DAY
        )
    )

Pct No Prazo =
    VAR Entregues =
        CALCULATE (
            DISTINCTCOUNT ( orders[order_id] ),
            NOT ISBLANK ( orders[order_delivered_customer_date] )
        )
    VAR NoPrazo =
        CALCULATE (
            DISTINCTCOUNT ( orders[order_id] ),
            orders[order_delivered_customer_date]
                <= orders[order_estimated_delivery_date]
        )
    RETURN DIVIDE ( NoPrazo, Entregues )
```

> **Único ponto de atenção na migração:** os nomes das tabelas mudam (`orders` → `fact_orders`, `order_items` → `fact_order_items`). A lógica DAX é **idêntica** — é exatamente essa a mensagem do comparativo antes/depois.
