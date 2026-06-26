import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


KEYWORDS = [
    "dragon ball",
    "dragonball",
    "fusion world",
    "dragon ball super"
]


def is_dragon_ball_product(name):
    name = name.lower()
    return any(keyword in name for keyword in KEYWORDS)


def check_magic_madhouse():
    store = "Magic Madhouse"
    search_url = "https://magicmadhouse.co.uk/search?q=dragon%20ball%20fusion%20world"

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers, timeout=25)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for link in soup.find_all("a", href=True):
        name = link.get_text(" ", strip=True)

        if not name:
            continue

        if not is_dragon_ball_product(name):
            continue

        product_url = urljoin(search_url, link["href"])
        
        if "/products/" not in product_url:
            continue
        products.append({
            "store": store,
            "name": name,
            "price": "Unknown",
            "url": product_url,
            "in_stock": True
        })

    return products


def get_all_products():
    products = []

    try:
        products.extend(check_magic_madhouse())
    except Exception as e:
        print(f"Magic Madhouse error: {e}")

    return products
