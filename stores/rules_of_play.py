from .shopify_json import check_shopify_json_store


def check_rules_of_play():
    return check_shopify_json_store(
        store_name="Rules of Play",
        base_url="https://rulesofplay.co.uk",
        search_query="dragon ball fusion world",
    )