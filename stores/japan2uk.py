from .shopify_json import check_shopify_json_store


def check_japan2uk():
    return check_shopify_json_store(
        store_name="Japan2UK",
        base_url="https://www.japan2uk.com",
        search_query="dragon ball fusion world",
    )