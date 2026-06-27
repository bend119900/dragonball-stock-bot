import time
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_page(url, timeout=25, retries=2, delay=1):
    last_error = None

    for attempt in range(retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            last_error = e
            print(f"Request failed: {url} | Attempt {attempt + 1}")
            time.sleep(delay)

    raise last_error


def get_soup(url):
    html = get_page(url)
    return BeautifulSoup(html, "html.parser")


def unique_by_url(products):
    unique = []
    seen = set()

    for product in products:
        url = product.get("url")

        if url not in seen:
            seen.add(url)
            unique.append(product)

    return unique