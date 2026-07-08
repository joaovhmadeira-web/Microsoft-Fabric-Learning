# Dados — Olist

Os dados brutos **não são versionados** (ver `.gitignore`). Este diretório contém apenas o script de preparação e, opcionalmente, amostras pequenas para inspeção.

## Fonte

- Dataset: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle)
- Licença: CC BY-NC-SA 4.0 — uso não comercial. Este projeto é educacional/portfólio.

## Tabelas em escopo (6)

| Nome no projeto | Arquivo Kaggle | Papel |
|---|---|---|
| `orders` | `olist_orders_dataset.csv` | Fato principal |
| `order_items` | `olist_order_items_dataset.csv` | Fato granularidade fina |
| `order_payments` | `olist_order_payments_dataset.csv` | Sensível → alvo de OLS |
| `customers` | `olist_customers_dataset.csv` | Dimensão |
| `sellers` | `olist_sellers_dataset.csv` | Dimensão (UF → eixo de RLS) |
| `products` | `olist_products_dataset.csv` | Dimensão |

## Como baixar

### Opção A — Kaggle API (recomendado)

```bash
pip install kaggle pandas
# coloque kaggle.json em ~/.kaggle/ (Linux/Mac) ou %USERPROFILE%\.kaggle\ (Windows)
python download_olist.py
```

### Opção B — zip baixado manualmente

Baixe o zip pela página do Kaggle e rode:

```bash
python download_olist.py --zip caminho/para/brazilian-ecommerce.zip
```

## Saída

```
data/
├── raw/       # 6 CSVs completos — NÃO versionar; subir como Bronze no Lakehouse
└── sample/    # amostras (1000 linhas) — ok versionar p/ inspeção rápida
```

## Próximo passo (Dia 1)

Subir os arquivos de `data/raw/` como camada **Bronze** no Lakehouse do Fabric (upload direto na UI ou via Dataflow Gen2 simples). Registrar as decisões em [`../docs/arquitetura.md`](../docs/arquitetura.md).
