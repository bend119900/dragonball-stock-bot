import requests


def looks_like_wanted_product(title):
    title = title.lower()

    if "dragon ball" not in title:
        return False

    wanted = [
        "fusion world",
        "booster box",
        "booster pack",
        "starter deck",
        "deck",
    ]

    ignored = [
        "sleeves",
        "accessories",
        "single",
        "common",
        "uncommon",
        "rare",
    ]

    return (
        any(word in title for word in wanted)
        and not any(word in title for word in ignored)
    )


def check_shopify_json_store(store_name, base_url, search_query):
    url = (
        f"{base_url.rstrip('/')}/search/suggest.json"
        f"?q={search_query.replace(' ', '%20')}"
        f"&resources[type]=product"
    )

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()
    items = data["resources"]["results"]["products"]

    products = []

    for item in items:
        title = item.get("title", "")

        if not looks_like_wanted_product(title):
            continue

        product_url = item.get("url", "")

        products.append({
            "store": store_name,
            "name": title,
            "price": f"£{item.get('price')}",
            "url": base_url.rstrip("/") + product_url,
            "in_stock": bool(item.get("available", False)),
        })

    print(f"{store_name} Shopify products found: {len(products)}")

    for product in products:
        print(
            f"Checked {store_name} product: {product['name']} | "
            f"Price: {product['price']} | "
            f"In stock: {product['in_stock']}"
        )

    return products