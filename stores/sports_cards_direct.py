from .shopify_json import check_shopify_json_store


def check_sports_cards_direct():
    return check_shopify_json_store(
        store_name="Sports Cards Direct",
        base_url="https://www.sportscardsdirect.co.uk",
        search_query="dragon ball fusion world",
    )