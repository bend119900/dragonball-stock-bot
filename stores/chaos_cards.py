import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


STORE_NAME = "Chaos Cards"
CATEGORY_URL = "https://www.chaoscards.co.uk/shop/card-games/dragonball-super-card-game/sealed-products-dragonball"


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
        "display",
        "premium",
        "pre-order",
        "preorder"
    ]

    excluded_words = [
        "sleeves",
        "binder",
        "playmat",
        "accessory",
        "common",
        "uncommon",
        "single"
    ]

    return (
        any(word in text for word in dragon_words)
        and any(word in text for word in sealed_words)
        and not any(word in text for word in excluded_words)
    )


def get_price(text):
    match = re.search(r"£\s?\d+(?:\.\d{2})?", text)
    if match:
        return match.group(0).replace(" ", "")
    return "Unknown"


def get_product_links():
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(CATEGORY_URL, headers=headers, timeout=25)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for link in soup.find_all("a", href=True):
        name = link.get_text(" ", strip=True)
        href = link["href"]

        if not name:
            continue

        if "/prod/" not in href:
            continue

        if not looks_like_product(name):
            continue

        product_url = urljoin(CATEGORY_URL, href)

        links.append({
            "name": name,
            "url": product_url
        })

    unique = []
    seen = set()

    for item in links:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)

    return unique


def check_product_page(item):
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(item["url"], headers=headers, timeout=25)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    text_lower = text.lower()

    out_of_stock_words = [
        "out of stock",
        "currently out of stock",
        "notify me",
        "we do not have enough stock available"
    ]

    in_stock_words = [
        "add to basket",
        "add to cart",
        "in stock"
    ]

    is_out_of_stock = any(word in text_lower for word in out_of_stock_words)
    has_buy_button = any(word in text_lower for word in in_stock_words)

    return {
        "store": STORE_NAME,
        "name": item["name"],
        "price": get_price(text),
        "url": item["url"],
        "in_stock": has_buy_button and not is_out_of_stock
    }


def check_chaos_cards():
    product_links = get_product_links()
    print(f"Chaos Cards product links found: {len(product_links)}")

    products = []

    for item in product_links:
        try:
            time.sleep(1)
            product = check_product_page(item)
            print(
                f"Checked Chaos product: {product['name']} | "
                f"Price: {product['price']} | "
                f"In stock: {product['in_stock']}"
            )
            products.append(product)
        except Exception as e:
            print(f"Error checking Chaos Cards product {item['url']}: {e}")

    return products