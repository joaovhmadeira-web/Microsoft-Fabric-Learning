<h1 align="center">Migração Power BI Legado → Microsoft Fabric</h1>

<p align="center">
  <em>Projeto end-to-end simulando uma migração enterprise de um ambiente Power BI (import mode) para o Microsoft Fabric — Lakehouse/OneLake, Direct Lake, Pipelines, Notebooks PySpark, RLS/OLS e FinOps.</em>
</p>

<p align="center">
  <img alt="Microsoft Fabric" src="https://img.shields.io/badge/Microsoft%20Fabric-0B7A75?style=for-the-badge&logo=microsoft&logoColor=white">
  <img alt="Power BI" src="https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black">
  <img alt="Delta Lake" src="https://img.shields.io/badge/Delta%20Lake-00ADD8?style=for-the-badge&logo=databricks&logoColor=white">
  <img alt="PySpark" src="https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="DAX" src="https://img.shields.io/badge/DAX-2C3E50?style=for-the-badge">
</p>

---

## Sobre o projeto

Este repositório documenta, de ponta a ponta, um projeto de **migração de dados e BI** de um ambiente **Power BI tradicional (import mode)** para a plataforma **Microsoft Fabric**. O objetivo é demonstrar, em escala reduzida mas realista, as competências técnicas e de negócio exigidas em projetos de migração enterprise: engenharia de dados, modelagem semântica, governança, performance/custos e a tradução técnico → negócio.

> O foco não é só "fazer funcionar", mas **documentar decisões de arquitetura, armadilhas reais e o comparativo antes/depois** — como num projeto de consultoria de verdade.

### Dataset

**[Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)** (público) — cenário real de marketplace: vendas, logística e pagamentos. Multi-tabela por natureza e com colunas sensíveis, perfeito para exercitar RLS/OLS. Escopo: 6 tabelas (`orders`, `order_items`, `order_payments`, `customers`, `sellers`, `products`).

---

## Arquitetura

Arquitetura **Medallion** (Bronze → Silver → Gold) sobre OneLake, com o modelo semântico em **Direct Lake**:

```
   CSV Olist
      │
      ▼
┌───────────────┐   Notebook PySpark   ┌───────────────┐   Notebook PySpark   ┌───────────────┐
│    BRONZE     │  ───────────────────▶ │    SILVER     │  ───────────────────▶ │     GOLD      │
│  raw / Delta  │  limpeza + tipagem    │ limpo, tipado │  modelagem estrela   │  dim_* / fact_*│
└───────────────┘                       └───────────────┘                       └───────┬───────┘
        Lakehouse `lh_olist` (OneLake)                                                   │
                                                                                          ▼
                                                                            ┌───────────────────────┐
                                                                            │   Modelo Direct Lake  │
                                                                            │   + RLS / OLS + DAX   │
                                                                            └───────────┬───────────┘
                                                                                        ▼
                                                                                Relatório Power BI

           Orquestração: Data Pipeline (Bronze → Silver → Gold, agendado)
           Operação:     Fabric Capacity Metrics (consumo de CU, SKU F)
```

### Comparativo: legado → Fabric

| Camada | Antes (legado) | Depois (Fabric) |
|---|---|---|
| **Ingestão** | CSVs manuais no PBI Desktop | Lakehouse **Bronze** (OneLake, Delta) |
| **Transformação** | Power Query no `.pbix` | Notebooks **PySpark** (Silver/Gold) + Pipeline |
| **Modelo semântico** | Import mode (dados duplicados) | **Direct Lake** sobre a Gold |
| **Segurança** | RLS básico | **RLS + OLS** governados |
| **Operação** | Refresh agendado, sem visibilidade de custo | Pipeline + **Capacity Metrics** (CU) |

---

## Stack técnica

| Área | Ferramentas |
|---|---|
| **Plataforma** | Microsoft Fabric (Lakehouse, OneLake, Pipelines, Notebooks) |
| **Engenharia de dados** | PySpark, Delta Lake, arquitetura Medallion |
| **Modelagem & BI** | Direct Lake, Power BI, DAX, esquema estrela |
| **Governança** | Row-Level Security (RLS), Object-Level Security (OLS) |
| **FinOps** | Fabric Capacity Metrics, dimensionamento de SKU F |
| **Prep local** | Python, pandas, Kaggle API |

---

## Roadmap (4 dias)

| Dia | Foco | Entregável | Status |
|---|---|---|:---:|
| **1** | Baseline legado + Lakehouse Bronze | `.pbix` import mode + Bronze no `lh_olist` | Concluído |
| **2** | Transformação Silver/Gold + Pipeline | Notebooks PySpark + Pipeline orquestrado | Concluído |
| **3** | Direct Lake + Segurança | Modelo Direct Lake com RLS/OLS testados | Pendente |
| **4** | Capacidade, custos & negócio | Capacity Metrics + plano de comunicação | Pendente |

---

## Estrutura do repositório

```
fabric-migration-olist/
├── README.md
├── data/                          # scripts de download/preparação (dados brutos NÃO versionados)
│   ├── download_olist.py
│   └── README.md
├── pbi-legacy/                    # modelo import mode — o "antes"
│   └── legacy_olist.pbix
├── notebooks/
│   ├── bronze_to_silver.ipynb     # limpeza + tipagem (PySpark)
│   └── silver_to_gold.ipynb       # modelagem dimensional (esquema estrela)
├── pipeline/                      # definição do Data Pipeline Fabric
├── docs/
│   ├── plano-projeto.md           # plano completo do projeto
│   ├── arquitetura.md             # Lakehouse vs Warehouse, Delta, particionamento
│   ├── seguranca-rls-ols.md       # papéis, DAX de RLS, matriz de teste
│   ├── capacidade-custos.md       # CU, SKU F, monitoramento
│   └── plano-comunicacao-migracao.md
└── dax/
    └── medidas.md                 # medidas DAX comentadas (versões Gold + legado)
```

---

## Destaques & aprendizados

- **Armadilha de qualidade de dados (locale decimal):** CSVs com `.` decimal + Power BI em pt-BR tipavam `price` como inteiro, inflando a receita em **×100** (R$ 1,36 bi vs. R$ 13,6 mi reais). Resolvido com `type number` + cultura `en-US` no `Table.TransformColumnTypes`. → [`pbi-legacy/README.md`](pbi-legacy/README.md)
- **Nuance de grão no RLS:** `seller_state` vive no grão de item, não de pedido — um pedido com sellers de estados diferentes aparece para múltiplos vendedores. Comportamento esperado de marketplace, documentado. → [`docs/seguranca-rls-ols.md`](docs/seguranca-rls-ols.md)
- **Direct Lake vs. Import:** mesma lógica DAX, mas sem cópia de dados nem refresh — leitura direta do Delta. → [`dax/medidas.md`](dax/medidas.md)
- **FinOps:** o divisor de águas de licenciamento é o **F64** (Power BI Pro grátis para consumidores). → [`docs/capacidade-custos.md`](docs/capacidade-custos.md)

---

## Como reproduzir

```bash
# 1. Baixar e preparar os dados (não versionados)
pip install -r requirements.txt
python data/download_olist.py        # requer credenciais do Kaggle

# 2. No Microsoft Fabric:
#    - criar Lakehouse `lh_olist` e subir data/raw/ como Bronze (brz_*)
#    - importar e rodar os notebooks (bronze_to_silver, silver_to_gold)
#    - criar o modelo Direct Lake sobre a Gold e aplicar RLS/OLS
```

Detalhes em [`data/README.md`](data/README.md) e [`docs/plano-projeto.md`](docs/plano-projeto.md).

---

## Métricas de negócio (DAX)

Receita total / por período · Ticket médio · % frete sobre venda · SLA de entrega (prazo real vs. promessa). Baseline validado: **Receita ~R$ 13,6 mi**, **Ticket ~R$ 137**, **% Frete ~20%**.

---

<p align="center">
  <sub>Projeto de estudo e portfólio · Dados públicos Olist (CC BY-NC-SA 4.0) · Uso não comercial</sub>
</p>
