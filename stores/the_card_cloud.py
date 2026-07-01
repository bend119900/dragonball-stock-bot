from .shopify_json import check_shopify_json_store


def check_the_card_cloud():
    return check_shopify_json_store(
        store_name="The Card Cloud",
        base_url="https://thecardcloud.co.uk",
        search_query="dragon ball fusion world",
    )