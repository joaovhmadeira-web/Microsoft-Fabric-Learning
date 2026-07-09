# Segurança — RLS & OLS (Dia 3)

Documentação da segurança aplicada ao modelo semântico **Direct Lake** sobre a camada Gold.

## RLS — Row-Level Security

**Cenário:** um vendedor só enxerga os pedidos que contêm itens vendidos por ele (eixo: estado/UF do seller).

> **Nuance de modelagem (grão):** `seller_id` / `seller_state` vivem no grão de **item** (`fact_order_items`), não em `fact_orders`. O filtro em `dim_seller` precisa propagar `dim_seller → fact_order_items`. Como um pedido pode conter itens de sellers de estados diferentes, esse pedido apareceria para **mais de um vendedor** — comportamento esperado de marketplace. Consequência prática: uma medida como `Receita Total` (baseada em `fact_order_items[price]`) filtra corretamente por vendedor; já medidas no grão de pedido (ex.: `DISTINCTCOUNT(fact_orders[order_id])`) podem contar um pedido "compartilhado" para dois estados. Validar no teste "View as role" e documentar o número esperado.

### Papéis

| Papel | Filtro | Uso |
|---|---|---|
| `Vendedor_SP` | `dim_seller[seller_state] = "SP"` | Exemplo estático de teste |
| `Vendedor_Dinamico` | `dim_seller[seller_state] = LOOKUPVALUE(...USERPRINCIPALNAME()...)` | Mapeamento usuário→UF via tabela de segurança |

### DAX do filtro (dinâmico)

```DAX
-- Regra na dim_seller (papel Vendedor_Dinamico)
dim_seller[seller_state] =
    LOOKUPVALUE(
        sec_user_uf[uf],
        sec_user_uf[email], USERPRINCIPALNAME()
    )
```

> Requer tabela auxiliar `sec_user_uf` (email → uf) na Gold. No trial, testar com "View as role" simulando UPN.

## OLS — Object-Level Security

**Cenário:** o papel "operacional" não pode ver o **valor de pagamento** (`payment_value`).

- Coluna alvo: `fact_orders[payment_value]` (e a medida `Receita Total` que a consome).
- No papel `Operacional`: definir a coluna/tabela como **restrita** (metadata: `None`).
- Efeito: a coluna some do modelo para esse papel; visuais que a usam quebram de forma controlada (esperado — documentar).

> OLS é editado via Tabular Editor (não há UI nativa no Power BI Desktop). Registrar o passo a passo.

## Matriz de teste (View as role)

| Papel | Vê pedidos de outros estados? | Vê `payment_value`? | Resultado esperado |
|---|---|---|---|
| Sem papel (admin) | Sim | Sim | Baseline |
| `Vendedor_SP` | Não (só SP) | Sim | RLS ok |
| `Operacional` | Sim | **Não** | OLS ok |
| `Vendedor_SP` + `Operacional` | Não (só SP) | Não | Combinação |

## A preencher durante execução

- [ ] Prints do "View as role" para cada linha da matriz
- [ ] Comportamento observado do Direct Lake com RLS (fallback p/ DirectQuery?)
- [ ] Limitações encontradas
