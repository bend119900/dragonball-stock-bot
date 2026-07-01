from .shopify_json import check_shopify_json_store


def check_the_card_vault():
    return check_shopify_json_store(
        store_name="The Card Vault",
        base_url="https://thecardvault.co.uk",
        search_query="dragon ball fusion world",
    )