import re
import time
from .base import get_soup
from bs4 import BeautifulSoup
from urllib.parse import urljoin


STORE_NAME = "Total Cards"
COLLECTION_URL = "https://totalcards.net/collections/dragon-ball-super-fusion-world-1"


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


def get_price(soup):
    price_tag = soup.select_one(".price-item.product-price")

    if price_tag:
        data_price = price_tag.get("data-price")
        if data_price:
            return f"£{data_price}"

        text_price = price_tag.get_text(" ", strip=True)
        if text_price:
            return text_price

    return "Unknown"


def get_product_links():
    soup = get_soup(COLLECTION_URL)
    links = []

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
    soup = get_soup(item["url"])
    text = soup.get_text(" ", strip=True)
    text_lower = text.lower()

    out_of_stock_words = [
        "sold out",
        "out of stock",
        "notify me when available",
        "unavailable"
    ]

    in_stock_words = [
        "add to cart",
        "add to basket",
        "buy it now",
        "pre-order",
        "preorder"
    ]

    is_out_of_stock = any(word in text_lower for word in out_of_stock_words)
    has_buy_button = any(word in text_lower for word in in_stock_words)

    in_stock = has_buy_button and not is_out_of_stock
    price = get_price(soup)

    return {
        "store": STORE_NAME,
        "name": item["name"],
        "price": price,
        "url": item["url"],
        "in_stock": in_stock
    }


def check_total_cards():
    product_links = get_product_links()
    print(f"Total Cards product links found: {len(product_links)}")

    products = []

    for item in product_links:
        try:
            time.sleep(1)
            product = check_product_page(item)
            print(
                f"Checked product: {product['name']} | "
                f"Price: {product['price']} | "
                f"In stock: {product['in_stock']}"
            )
            products.append(product)
        except Exception as e:
            print(f"Error checking product page {item['url']}: {e}")

    return products