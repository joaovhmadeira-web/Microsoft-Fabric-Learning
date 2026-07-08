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

## A versionar aqui

- `.pbix` (ou formato `.pbip` / export do modelo). **Não** subir dados brutos.
- Print do relatório publicado (para o README).
