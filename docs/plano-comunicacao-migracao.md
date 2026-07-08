# Plano de comunicação de migração (Dia 4)

> Documento de 1 página voltado a **áreas de negócio** — tradução técnico → negócio.

## O que está mudando

Estamos movendo os relatórios de vendas/logística do ambiente Power BI atual para o **Microsoft Fabric**. Para o usuário final, os relatórios continuam os mesmos; o que muda é a "usina" por trás: dados mais frescos, mais governança e custo previsível.

## O que muda para o usuário final

| Aspecto | Antes | Depois | Impacto |
|---|---|---|---|
| Atualização dos dados | Refresh agendado (dados podiam ficar horas defasados) | **Direct Lake** — próximo do tempo real | Positivo |
| Acesso a dados sensíveis | Controle limitado | **RLS/OLS** — cada um vê o que pode | Positivo (compliance) |
| Aparência dos relatórios | — | Igual | Nenhum |
| Endereço/link | Workspace antigo | Novo workspace Fabric | Atualizar favoritos |

## Riscos & mitigação

| Risco | Mitigação |
|---|---|
| Divergência de números antes/depois | Período de **validação em paralelo** (rodar os dois e conferir métricas-chave) |
| Usuário sem acesso pós-migração | Mapear papéis/permissões antes do corte |
| Coluna sensível exposta indevidamente | Teste de OLS documentado (ver `seguranca-rls-ols.md`) |
| Quebra de link/favorito | Comunicado com novo link + redirecionamento temporário |

## Janela de corte (cutover)

1. **Congelamento** do modelo legado (sem novas mudanças).
2. **Validação em paralelo** (X dias): comparar Receita, Ticket médio, SLA de entrega.
3. **Corte** em janela de baixo uso; legado em modo somente-leitura por 2 semanas.
4. **Desativação** do legado após sign-off do negócio.

## Comunicação — quem e quando

| Público | Canal | Quando |
|---|---|---|
| Diretoria/sponsors | Resumo executivo | Antes do corte |
| Usuários dos relatórios | E-mail + treinamento curto | 1 semana antes |
| TI/Suporte | Runbook de cutover | Dia do corte |

## Métricas de sucesso

- Paridade de números na validação (Receita, Ticket médio, % frete, SLA).
- 0 incidentes de acesso indevido a dado sensível.
- Adoção: % de usuários acessando o novo workspace na 1ª semana.
