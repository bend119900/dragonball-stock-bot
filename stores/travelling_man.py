from .shopify_json import check_shopify_json_store


def check_travelling_man():
    return check_shopify_json_store(
        store_name="Travelling Man",
        base_url="https://travellingman.com",
        search_query="dragon ball fusion world",
    )