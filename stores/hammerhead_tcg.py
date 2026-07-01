from .shopify_json import check_shopify_json_store


def check_hammerhead_tcg():
    return check_shopify_json_store(
        store_name="Hammerhead TCG",
        base_url="https://www.hammerheadtcg.co.uk",
        search_query="dragon ball fusion world",
    )