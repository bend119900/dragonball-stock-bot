from stores.shopify_store import test_shopify_products_json

stores = [
    ("Magic Madhouse", "https://magicmadhouse.co.uk"),
    ("Travelling Man", "https://travellingman.com"),
    ("Card Vault", "https://www.cardvault.co.uk"),
]

for name, url in stores:
    print()
    print("━━━━━━━━━━━━━━━━━━━━")
    test_shopify_products_json(name, url)