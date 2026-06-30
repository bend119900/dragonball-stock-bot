import requests


def test_shopify_products_json(store_name, base_url):
    url = f"{base_url.rstrip('/')}/products.json?limit=10"

    print(f"Testing {store_name}: {url}")

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        print("Status:", response.status_code)

        if response.status_code != 200:
            return []

        data = response.json()
        products = data.get("products", [])

        print(f"Products found: {len(products)}")

        for product in products[:5]:
            print("-", product.get("title"))

        return products

    except Exception as e:
        print(f"Error testing {store_name}: {e}")
        return []