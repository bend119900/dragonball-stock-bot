from .shopify_json import check_shopify_json_store


def check_the_vault_tcg():
    return check_shopify_json_store(
        store_name="The Vault TCG",
        base_url="https://thevaulttcg.co.uk",
        search_query="dragon ball fusion world",
    )