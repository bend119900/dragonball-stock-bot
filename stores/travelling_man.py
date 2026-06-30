import requests

STORE_NAME = "Travelling Man"
SEARCH_URL = "https://travellingman.com/search/suggest.json?q=dragon%20ball%20fusion%20world&resources[type]=product"
BASE_URL = "https://travellingman.com"


def looks_like_product(title):
    title = title.lower()

    if "dragon ball" not in title:
        return False

    wanted = [
        "booster box",
        "booster pack",
        "starter deck",
    ]

    ignored = [
        "sleeves",
        "accessories",
        "manga",
    ]

    return (
        any(word in title for word in wanted)
        and not any(word in title for word in ignored)
    )


def check_travelling_man():
    response = requests.get(
        SEARCH_URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()
    items = data["resources"]["results"]["products"]

    products = []

    for item in items:
        title = item.get("title", "")

        if not looks_like_product(title):
            continue

        products.append({
            "store": STORE_NAME,
            "name": title,
            "price": f"£{item.get('price')}",
            "url": BASE_URL + item.get("url", ""),
            "in_stock": item.get("available", False),
        })

    print(f"Travelling Man products found: {len(products)}")

    for product in products:
        print(
            f"Checked Travelling Man product: {product['name']} | "
            f"Price: {product['price']} | "
            f"In stock: {product['in_stock']}"
        )

    return products