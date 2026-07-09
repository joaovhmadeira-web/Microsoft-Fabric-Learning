# pbi-legacy — o "antes" (Dia 1)

Modelo Power BI Desktop tradicional (**import mode**) que representa o ambiente legado a ser migrado.

## Escopo (deliberadamente simples)

- 2-3 tabelas importadas (ex.: `orders`, `order_items`, `customers`) via Power Query dos CSVs.
- 3-4 medidas DAX de [`../dax/medidas.md`](../dax/medidas.md): Receita Total, Ticket Médio, % Frete, SLA de entrega.
- **Não refinar** — serve só como baseline de comparação para o Direct Lake (Dia 3).

## Passos

1. Power BI Desktop → *Get Data* → CSV (`data/raw/`).
2. Modelar relacionamentos básicos (orders ↔ order_items ↔ customers).
3. Criar as medidas.
4. Publicar no workspace do projeto.

## Pegadinha de qualidade de dados — locale decimal

Os CSVs do Olist usam **ponto** como separador decimal (`58.90`). Com o Power BI em **português (Brasil)**, a etapa automática "Tipo Alterado" do Power Query lê o `.` como separador de **milhar** e tipa `price`/`freight_value` como `Int64.Type`, gerando valores **×100** (Receita Total dava ~R$ 1,36 **bilhão** em vez de ~R$ 13,6 milhões).

**Correção** (Power Query → `order_items` → passo de tipo):
```m
// de: {"price", Int64.Type}, {"freight_value", Int64.Type}   ...})
// para: {"price", type number}, {"freight_value", type number}   ...}, "en-US")
```
O terceiro argumento `"en-US"` de `Table.TransformColumnTypes` força o `.` como separador decimal.

> Bom exemplo de problema real de migração para citar na entrevista.

## Baseline validado (números esperados)

| Medida | Valor aproximado |
|---|---|
| Receita Total | ~R$ 13,6 milhões |
| Ticket Médio | ~R$ 137 |
| % Frete s/ Venda | ~20% |

## A versionar aqui

- `.pbix` (ou formato `.pbip` / export do modelo). **Não** subir dados brutos.
- Print do relatório publicado (para o README).
