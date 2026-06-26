import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


STORE_NAME = "Total Cards"
COLLECTION_URL = "https://totalcards.net/collections/dragon-ball-super-fusion-world-1"

PRODUCT_WORDS = [
    "dragon ball",
    "fusion world",
    "dragon ball super",
    "booster",
    "starter",
    "deck",
    "pack",
    "box",
    "pre-release",
    "premium",
]


def looks_like_product(text):
    text = text.lower()

    dragon_words = [
        "dragon ball",
        "dragonball",
        "fusion world",
        "dragon ball super"
    ]

    sealed_words = [
        "booster",
        "booster box",
        "booster pack",
        "starter",
        "deck",
        "energy marker",
        "pre-release",
        "premium"
    ]

    excluded_words = [
        "common",
        "uncommon",
        "rare",
        "tournament pack"
    ]

    return (
        any(word in text for word in dragon_words)
        and any(word in text for word in sealed_words)
        and not any(word in text for word in excluded_words)
    )


def check_total_cards():
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(COLLECTION_URL, headers=headers, timeout=25)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for link in soup.find_all("a", href=True):
        name = link.get_text(" ", strip=True)
        href = link["href"]

        if not name:
            continue

        if "/products/" not in href:
            continue

        if not looks_like_product(name):
            continue

        product_url = urljoin(COLLECTION_URL, href)

        product_text = link.parent.get_text(" ", strip=True).lower()

out_of_stock_words = [
    "sold out",
    "out of stock",
    "notify me",
    "unavailable"
]

in_stock = not any(word in product_text for word in out_of_stock_words)

products.append({
    "store": STORE_NAME,
    "name": name,
    "price": "Unknown",
    "url": product_url,
    "in_stock": in_stock
})

    # Remove duplicates
    unique = []
    seen = set()

    for product in products:
        key = product["url"]
        if key not in seen:
            seen.add(key)
            unique.append(product)

    return unique
