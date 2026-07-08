# Capacidade, performance & custos (Dia 4)

## Objetivo

Mostrar visão de operação/FinOps: consumo de **Capacity Units (CU)**, dimensionamento de **SKU F** e o que monitorar em produção.

## Ferramenta

**Microsoft Fabric Capacity Metrics App** (instalar via AppSource no workspace/capacity trial).

## Exercício

1. Rodar carga pesada: reprocessar o Pipeline inteiro (Bronze→Silver→Gold) + refresh/consultas Direct Lake.
2. Abrir o Capacity Metrics App e observar:
   - Pico de CU por operação (Spark notebook vs. Dataflow vs. query semântica).
   - *Throttling* / *smoothing* (Fabric distribui o consumo no tempo).
   - Operações "interactive" vs. "background".

## Dimensionamento de SKU F

Referência de CU por SKU (capacity):

| SKU | CU | Nota |
|---|---|---|
| F2 | 2 | Dev/POC pequeno |
| F4 | 4 | — |
| F8 | 8 | Times pequenos |
| F64 | 64 | **Habilita Power BI Pro grátis p/ consumidores** (marco importante de licenciamento) |

**Para este cenário (dataset pequeno, uso intermitente):** F2–F4 sustentaria as transformações; o gargalo real é o pico de Spark durante o reprocessamento, não o volume de dados. Em produção com N relatórios/consumidores, o divisor de águas é **F64** pelo licenciamento.

## O que monitorar em produção

- CU médio vs. pico e frequência de *throttling*.
- Custo de refresh Direct Lake vs. import.
- Jobs Spark caros (pool size, tempo de startup).
- *Autoscale* / pausar capacity fora do horário (economia real no F SKU).

## A preencher durante execução

- [ ] Print do Capacity Metrics após reprocessamento
- [ ] CU pico observado + operação que gerou
- [ ] Recomendação de SKU justificada
