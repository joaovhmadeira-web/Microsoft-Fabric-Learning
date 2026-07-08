# Fabric Migration — Olist

Simulação, em escala reduzida, de um projeto de migração *enterprise* de um ambiente **Power BI legado (import mode)** para o **Microsoft Fabric** (Lakehouse/OneLake, Direct Lake, Pipelines/Notebooks/Dataflows Gen2, RLS/OLS e governança, capacidade/custos).

> Dataset: **Olist Brazilian E-Commerce** (público, Kaggle). Apenas dados públicos/sintéticos, isolados em workspace dedicado.

## Narrativa: legado → Fabric

| Camada | Antes (legado) | Depois (Fabric) |
|---|---|---|
| Ingestão | CSVs manuais no PBI Desktop | Lakehouse **Bronze** (OneLake, Delta) |
| Transformação | Power Query no .pbix | Notebooks PySpark **Silver/Gold** + Pipeline |
| Modelo semântico | Import mode (dados duplicados no dataset) | **Direct Lake** sobre a camada Gold |
| Segurança | RLS básico no .pbix | **RLS + OLS** no modelo semântico Fabric |
| Operação | Refresh agendado, sem visibilidade de custo | Pipeline + **Capacity Metrics** (CU) |

## Escopo de tabelas

`orders` (fato) · `order_items` (fato granular) · `order_payments` (sensível → OLS) · `customers` · `sellers` (UF → eixo de RLS) · `products`

## Estrutura do repositório

```
fabric-migration-olist/
├── README.md                      # esta narrativa, decisões, prints
├── data/                          # scripts de download/preparação (dados brutos NÃO versionados)
│   ├── download_olist.py
│   └── README.md
├── pbi-legacy/                    # modelo import mode (Dia 1) — o "antes"
├── notebooks/
│   ├── bronze_to_silver.ipynb     # Dia 2
│   └── silver_to_gold.ipynb       # Dia 2
├── pipeline/                      # export/definição do Pipeline Fabric (Dia 2)
├── docs/
│   ├── arquitetura.md
│   ├── seguranca-rls-ols.md
│   ├── capacidade-custos.md
│   └── plano-comunicacao-migracao.md
└── dax/
    └── medidas.md                 # medidas DAX comentadas (antes/depois)
```

## Progresso

- [x] Esqueleto do repositório
- [x] **Dia 1** — Baseline PBI legado + Lakehouse Bronze
- [ ] **Dia 2** — Silver/Gold (Notebooks) + Pipeline
- [ ] **Dia 3** — Direct Lake + RLS/OLS
- [ ] **Dia 4** — Capacidade/custos + camada de negócio

## Como começar

1. Baixar os dados: veja [`data/README.md`](data/README.md).
2. Subir os 6 CSVs como camada Bronze no Lakehouse (upload direto ou Dataflow Gen2 simples).
3. Registrar decisões de arquitetura em [`docs/arquitetura.md`](docs/arquitetura.md).
