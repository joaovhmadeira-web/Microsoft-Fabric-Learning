# Capacidade, performance & custos (Dia 4)

## Objetivo

Mostrar visão de operação/FinOps: consumo de **Capacity Units (CU)**, dimensionamento de **SKU F** e o que monitorar em produção.

## Ferramenta

**Microsoft Fabric Capacity Metrics App** (AppSource) — ferramenta padrão para CU/throttling.

> **Limitação encontrada (ambiente trial):** o Metrics App **não conecta à capacity trial (FT)** deste tenant — retorna `QueryUserError: Error obtaining data location`. O app pressupõe uma capacity paga (F/P SKU) com admin de capacity. Em produção, com uma F SKU, o app funciona normalmente.
>
> **Plano B usado:** observação de consumo pelo **Monitoring Hub** (durações reais de pipeline e notebooks Spark), que funciona no trial, + análise de dimensionamento abaixo. O gargalo de CU é inferido a partir da atividade mais cara (pico de Spark no reprocessamento).

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

## Observações reais (Monitoring Hub, execução de 2026-07-12)

Reprocessamento completo do pipeline `pl_olist_medallion` — status **Bem-sucedido**:

| Atividade | Duração | Observação |
|---|---|---|
| `nb_bronze_to_silver` | **2m 13s** | limpeza/tipagem/joins Silver |
| `nb_silver_to_gold` | **2m 10s** | modelagem dimensional (mais joins) |
| **Pipeline total** | **~4m 24s** | notebooks em sequência (On success) |

**Leitura do resultado:** as duas atividades levaram **praticamente o mesmo tempo (~2min)** apesar de o silver→gold fazer mais transformações. Ou seja, o tempo é dominado pelo **overhead de sessão Spark** (startup + orquestração), **não pelo volume de dados** — que aqui é minúsculo. 

**Implicação de custo/CU:** neste cenário, o consumo é dirigido pelo **compute Spark por execução**, não pelo tamanho do dado. Alavancas que realmente reduzem custo: (1) **reutilização de sessão** / *high-concurrency pools* para não pagar startup a cada notebook; (2) **pausar a capacity** fora da janela do pipeline (agendado 03:00); (3) starter pool vs. custom pool. Aumentar SKU **não** melhoraria o tempo aqui — o gargalo é overhead fixo, não falta de CU.

## Recomendação de SKU (justificada)

- **Transformação (este dataset):** **F2** sustenta o pipeline com folga; o gargalo é overhead de sessão, não CU.
- **Produção real (N consumidores):** o divisor de águas é **F64** — não por performance, mas por **licenciamento** (habilita Power BI Pro grátis para os consumidores). Abaixo de F64, cada consumidor precisa de licença Pro.
- **Regra prática:** dimensionar pela **camada de consumo/licenciamento**, não pelo volume de transformação — no Olist o dado cabe em qualquer SKU.

## Pendências

- [x] Carga pesada reprocessada e medida (Monitoring Hub)
- [x] Gargalo identificado (overhead de sessão Spark) + recomendação de SKU
- [ ] (opcional) Print do Monitoring Hub anexado em `prints/`
- ~~Print do Capacity Metrics~~ — inviável no trial (ver limitação acima)
