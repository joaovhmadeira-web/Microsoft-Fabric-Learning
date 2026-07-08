# pipeline — orquestração Fabric (Dia 2)

Definição/export do **Data Pipeline** que orquestra Bronze → Silver → Gold.

## Fluxo

```
[Notebook bronze_to_silver] ──► [Notebook silver_to_gold] ──► (opcional) refresh do modelo semântico
```

- Atividades: dois *Notebook activities* em sequência (sucesso → próximo).
- **Agendamento configurado** (não precisa rodar em produção — só existir configurado, ex.: diário 03:00).
- Conectar o workspace ao **Git do Fabric** para versionar notebooks + pipeline.

## A versionar aqui

- Export JSON da definição do pipeline (via Git integration ou "Save as").
- Print da tela do pipeline e da configuração de agendamento.
