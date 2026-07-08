# Projeto: Migração de Ambiente Power BI Legado para Microsoft Fabric

## Objetivo

Simular, em escala reduzida, um projeto de migração enterprise de workspaces/datasets/relatórios Power BI para o Microsoft Fabric, cobrindo as competências técnicas e de negócio exigidas para a vaga de referência (migração, Lakehouse/OneLake, Direct Lake, Dataflows Gen2/Pipelines/Notebooks, RLS/OLS e governança, capacidade/performance/custos, e tradução técnico-negócio).

**Prazo:** 4 dias (~3-4h/dia)
**Ambiente:** Fabric trial capacity (conta corporativa) — usar apenas dados públicos/sintéticos, isolar em workspace dedicado ao projeto.

## Dataset

**Olist Brazilian E-Commerce Dataset** (público, Kaggle) — cenário de negócio real (marketplace, vendas, logística, pagamentos), naturalmente multi-tabela, com colunas sensíveis para exercitar RLS/OLS.

### Escopo de tabelas (usar apenas estas)
- `orders` — fato principal
- `order_items` — fato de granularidade fina
- `order_payments` — sensível, alvo de OLS
- `customers`
- `sellers` — com UF/estado, eixo de RLS
- `products`

**Fora de escopo:** reviews, geolocation detalhada, tradução de categorias — não agregam ao teste de habilidades Fabric.

### Métricas de negócio (DAX)
- Receita total / receita por período
- Ticket médio
- % frete sobre valor da venda
- Prazo de entrega vs. promessa (SLA de entrega)

## Plano de execução

### Dia 1 — Baseline "legado" + Lakehouse (Bronze)
**Objetivo:** ter algo pra "migrar" e iniciar a ingestão.

1. (1h) Modelo no Power BI Desktop tradicional (import mode), 2-3 tabelas, 3-4 medidas DAX — este é o "antes" (comparação futura), não precisa ser refinado.
2. (2h) No Fabric: criar Lakehouse, subir CSVs brutos como camada **Bronze** (upload direto ou Dataflow Gen2 simples).
3. (30min) Documentar decisões: Lakehouse vs. Warehouse, formato de arquivos, particionamento.

**Entrega:** Lakehouse com dados brutos + relatório PBI legado publicado.

### Dia 2 — Transformação (Silver/Gold) + Pipeline
**Objetivo:** pipeline de dados funcional, ponta a ponta.

1. (2h) Notebook PySpark: limpeza, tipagem, joins básicos → camada **Silver**.
2. (1h) Notebook ou Dataflow Gen2: modelagem dimensional final (fato + dimensões conformadas) → camada **Gold**, em Delta.
3. (1h) Orquestrar em um **Pipeline** (Bronze→Silver→Gold), com agendamento configurado (não precisa rodar em produção, só existir configurado).

**Entrega:** Pipeline funcional Bronze→Silver→Gold + notebooks versionados (conectar workspace ao Git do Fabric).

### Dia 3 — Direct Lake + Segurança
**Objetivo:** o núcleo técnico da vaga.

1. (1,5h) Criar dataset semântico em **Direct Lake** sobre a camada Gold, recriando as medidas DAX do Dia 1.
2. (30min) Comparar import mode vs. Direct Lake (refresh, comportamento de agregações, limites conhecidos).
3. (1h) Implementar **RLS** (ex: vendedor só vê pedidos do seu estado) e **OLS** (ex: esconder coluna de valor de pagamento para papel "operacional").
4. (30min) Testar como usuário diferente ("view as role") e documentar.

**Entrega:** Modelo Direct Lake com RLS/OLS ativos e testados.

### Dia 4 — Capacidade, custos e camada de negócio
**Objetivo:** mostrar visão além do técnico.

1. (1h) Instalar o app **Fabric Capacity Metrics**, rodar carga mais pesada (reprocessar pipeline inteiro), observar consumo de CU.
2. (30min) Nota curta: dimensionamento de SKU F para o cenário e o que monitorar em produção.
3. (1h) Documento de 1 página: plano de comunicação de migração para áreas de negócio (o que muda para o usuário final, riscos, janela de corte).
4. (1h) Fechar README/relatório consolidado: prints, decisões de arquitetura, comparativo antes/depois.

**Entrega:** Pacote fechado, pronto para discussão em entrevista.

## Checklist — cobertura da vaga

| Requisito da vaga | Onde aparece no projeto |
|---|---|
| Migração de workspaces/datasets/relatórios | Dia 1 (baseline) → Dia 3 (Direct Lake) |
| Lakehouse + OneLake + Direct Lake | Dia 1, Dia 3 |
| Dataflows Gen2, Pipelines, Notebooks | Dia 2 |
| RLS/OLS, governança de dados | Dia 3 |
| Capacidade/performance/custos (F SKUs) | Dia 4 |
| Tradução técnico→negócio, change management | Dia 4 |
| DAX avançado, modelagem semântica | Dia 1, Dia 3 |
| SQL/PySpark | Dia 2 |

## Estrutura sugerida do repositório

```
fabric-migration-olist/
├── README.md                      # narrativa "legado → Fabric", decisões, prints
├── data/                          # amostras/scripts de download do Olist (não versionar dados brutos completos)
├── pbi-legacy/                    # .pbix ou export do modelo import mode (Dia 1)
├── notebooks/
│   ├── bronze_to_silver.ipynb
│   └── silver_to_gold.ipynb
├── pipeline/                      # definição/export do pipeline Fabric
├── docs/
│   ├── arquitetura.md             # Lakehouse vs Warehouse, particionamento, decisões
│   ├── seguranca-rls-ols.md
│   ├── capacidade-custos.md
│   └── plano-comunicacao-migracao.md
└── dax/
    └── medidas.md                 # medidas DAX comentadas (antes/depois)
```
