import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


STORE_NAME = "Zatu Games"
CATEGORY_URL = "https://zatu.com/collections/dragon-ball"


def looks_like_product(text):
    text = text.lower()

    dragon_words = ["dragon ball", "dragonball", "fusion world"]
    sealed_words = ["booster", "box", "pack", "starter", "deck", "premium"]

    excluded_words = [
        "sleeves",
        "card case",
        "accessory",
        "playmat",
        "single",
    ]

    return (
        any(word in text for word in dragon_words)
        and any(word in text for word in sealed_words)
        and not any(word in text for word in excluded_words)
    )


def get_price(soup):
    price_tag = soup.select_one(".f-price-item--sale")

    if price_tag:
        price = price_tag.get_text(" ", strip=True)
        if price:
            return price

    text = soup.get_text(" ", strip=True)
    match = re.search(r"£\s?\d+(?:\.\d{2})?", text)
    return match.group(0).replace(" ", "") if match else "Unknown"


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

        if "/products/" not in href:
            continue

        if not looks_like_product(name):
            continue

        links.append({
            "name": name,
            "url": urljoin(CATEGORY_URL, href)
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

    button = soup.select_one("button[name='add']")
    button_text = button.get_text(" ", strip=True).lower() if button else ""

    page_text = soup.get_text(" ", strip=True).lower()

    out_words = [
        "out of stock",
        "sold out",
        "currently unavailable",
        "notify me when available"
    ]

    in_stock = (
        button is not None
        and "add to basket" in button_text
        and not button.has_attr("disabled")
        and not any(word in page_text for word in out_words)
    )

    return {
        "store": STORE_NAME,
        "name": item["name"],
        "price": get_price(soup),
        "url": item["url"],
        "in_stock": in_stock
    }


def check_zatu():
    product_links = get_product_links()
    print(f"Zatu product links found: {len(product_links)}")

    products = []

    for item in product_links:
        try:
            time.sleep(1)
            product = check_product_page(item)
            print(
                f"Checked Zatu product: {product['name']} | "
                f"Price: {product['price']} | "
                f"In stock: {product['in_stock']}"
            )
            products.append(product)
        except Exception as e:
            print(f"Error checking Zatu product {item['url']}: {e}")

    return products