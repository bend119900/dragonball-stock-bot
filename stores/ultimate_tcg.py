from .shopify_json import check_shopify_json_store


def check_ultimate_tcg():
    return check_shopify_json_store(
        store_name="Ultimate TCG",
        base_url="https://www.ultimatetcg.co.uk",
        search_query="dragon ball fusion world",
    )