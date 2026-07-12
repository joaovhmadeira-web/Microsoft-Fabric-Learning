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

#### Criar a tabela `sec_user_uf` (rodar no notebook, Lakehouse schema-enabled)

```python
from pyspark.sql import Row

# email do usuario -> UF que ele pode enxergar. Ajustar para os UPNs reais do tenant.
sec_rows = [
    Row(email="joao.madeira@gradusconsultoria.com.br", uf="SP"),
    Row(email="vendedor.rj@gradusconsultoria.com.br", uf="RJ"),  # ficticio, so p/ demonstrar 2o mapeamento
]
sec = spark.createDataFrame(sec_rows)
sec.write.mode("overwrite").format("delta").saveAsTable(tbl("gold_sec_user_uf"))
```

> A tabela entra no modelo semântico como `sec_user_uf` (renomear removendo o prefixo `gold_`, igual às demais). **Não** crie relacionamento dela com `dim_seller`; ela é consultada só via `LOOKUPVALUE` no filtro do papel. Marque-a como oculta no modelo.

## OLS — Object-Level Security

**Cenário:** o papel "operacional" não pode ver o **valor de pagamento** (`payment_value`).

- Coluna alvo: `fact_orders[payment_value]` (e a medida `Receita Total` que a consome).
- No papel `Operacional`: definir a coluna como **restrita** (permission: `None`).
- Efeito: a coluna some do modelo para esse papel; a medida de demonstração `Total Pagamentos` (= `SUM(fact_orders[payment_value])`) quebra de forma controlada para esse papel (esperado — documentar).

### Método usado: `semantic-link-labs` (não Tabular Editor)

OLS não tem UI nativa no editor web nem no Power BI Desktop. O caminho padrão seria o **Tabular Editor**, mas o **TE2 (gratuito) falha ao salvar em modelos Direct Lake** (`"The given key was not present in the dictionary"` — falha de serialização do cliente, não bloqueio de XMLA; o TE3 pago contorna). 

Solução adotada (melhor para o portfólio: código versionável, roda no próprio notebook Fabric):

```python
from sempy_labs.tom import connect_semantic_model

dataset, workspace = "sm_olist_gold", "Fabric Learning"

with connect_semantic_model(dataset=dataset, workspace=workspace, readonly=False) as tom:
    try:
        tom.add_role(role_name="Operacional", model_permission="Read")
    except Exception:
        pass  # papel ja existe
    try:
        tom.add_measure(table_name="fact_orders", measure_name="Total Pagamentos",
                        expression="SUM ( fact_orders[payment_value] )")
    except Exception:
        pass  # medida ja existe
    tom.set_ols(role_name="Operacional", table_name="fact_orders",
                column_name="payment_value", permission="None")
```

> Instalar antes: `%pip install semantic-link-labs`. O commit no modelo publicado acontece ao sair do bloco `with`. Nomes de papéis são case-sensitive no TOM (ficaram em minúsculas: `operacional`).

## Teste de segurança — método e resultados

### Como foi testado (e por que não pelo caminho padrão)

Os dois simuladores nativos **não funcionam** neste modelo Direct Lake:

- **Power BI Desktop → "Exibir como"**: desabilitado em *live connection* a modelo publicado (papéis vivem no modelo remoto, não local).
- **Serviço → "Test as role"**: falha com `"não funciona com o logon único (SSO)"` — o Direct Lake lê o Lakehouse via SSO e o preview não consegue impersonar por cima dessa conexão.

**Validado via DAX Studio** conectado ao endpoint XMLA (`powerbi://api.powerbi.com/v1.0/myorg/Fabric Learning`), usando **Advanced Options → Roles + Effective User Name** para impersonar. Queries de verificação:

```DAX
EVALUATE ROW ( "Receita", [Receita Total], "Pagamentos", [Total Pagamentos] )
EVALUATE SUMMARIZECOLUMNS ( dim_seller[seller_state], "Receita", [Receita Total] )
```

### Resultados (matriz de teste)

| Papel (Roles) | Effective User Name | `seller_state` na tabela | `[Total Pagamentos]` | Resultado |
|---|---|---|---|---|
| *(nenhum)* | — | todos | mostra valor | Baseline |
| `Vendedor_SP` | — | **só SP** | mostra valor | **RLS estático OK** |
| `Vendedor_Dinamico` | `joao.madeira@gradusconsultoria.com.br` | **só SP** (via `sec_user_uf`) | mostra valor | **RLS dinâmico OK** |
| `Operacional` | — | todos | **erro (coluna restrita)** | **OLS OK** |

Confirmado em 2026-07-11.

## Limitações & observações

- "Test as role" do serviço é incompatível com SSO em Direct Lake → testar por XMLA (DAX Studio) ou impersonação via código.
- OLS em Direct Lake **não** é editável pelo Tabular Editor 2 gratuito (falha de serialização) → aplicado via `semantic-link-labs`.
- [ ] (opcional) Anexar prints do DAX Studio de cada papel.
