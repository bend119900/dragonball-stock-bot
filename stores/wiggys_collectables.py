from .shopify_json import check_shopify_json_store


def check_wiggys_collectables():
    return check_shopify_json_store(
        store_name="Wiggy's Collectables",
        base_url="https://wiggyscollectables.co.uk",
        search_query="dragon ball fusion world",
    )