# Seguranca como codigo (Dia 3) — RLS + OLS no modelo Direct Lake
#
# Reproduz toda a camada de seguranca do modelo semantico "sm_olist_gold"
# de forma programatica, via semantic-link-labs. Rodar num notebook Fabric
# anexado ao workspace "Fabric Learning".
#
# Contexto: o Tabular Editor 2 (gratuito) falha ao salvar OLS em modelos
# Direct Lake ("The given key was not present in the dictionary"). Este
# script e o Plano B — e, de quebra, deixa a seguranca versionavel no Git,
# ja que a integracao Git nativa do Fabric esta bloqueada pelo tenant.
#
# Pre-requisito: %pip install semantic-link-labs

from sempy_labs.tom import connect_semantic_model

DATASET   = "sm_olist_gold"
WORKSPACE = "Fabric Learning"

# email/UPN -> UF resolvido pela tabela gold_sec_user_uf (LOOKUPVALUE)
RLS_DINAMICO = (
    '[seller_state] = '
    'LOOKUPVALUE ( sec_user_uf[uf], sec_user_uf[email], USERPRINCIPALNAME() )'
)


def _try(fn, *args, **kwargs):
    """Executa e ignora 'ja existe' — deixa o script idempotente."""
    try:
        fn(*args, **kwargs)
    except Exception as e:
        print("  (ignorado:", type(e).__name__, ")")


with connect_semantic_model(dataset=DATASET, workspace=WORKSPACE, readonly=False) as tom:
    print("Papeis antes:", [r.Name for r in tom.model.Roles])

    # --- RLS estatico: vendedor so ve o proprio estado (exemplo fixo SP) ---
    _try(tom.add_role, role_name="Vendedor_SP", model_permission="Read")
    tom.set_rls(role_name="Vendedor_SP", table_name="dim_seller",
                filter_expression='[seller_state] = "SP"')

    # --- RLS dinamico: UF resolvida pelo UPN via sec_user_uf ---
    _try(tom.add_role, role_name="Vendedor_Dinamico", model_permission="Read")
    tom.set_rls(role_name="Vendedor_Dinamico", table_name="dim_seller",
                filter_expression=RLS_DINAMICO)

    # --- OLS: esconde payment_value do papel Operacional ---
    _try(tom.add_role, role_name="Operacional", model_permission="Read")
    _try(tom.add_measure, table_name="fact_orders", measure_name="Total Pagamentos",
         expression="SUM ( fact_orders[payment_value] )")
    tom.set_ols(role_name="Operacional", table_name="fact_orders",
                column_name="payment_value", permission="None")

    print("Papeis depois:", [r.Name for r in tom.model.Roles])

print("Camada de seguranca aplicada.")
