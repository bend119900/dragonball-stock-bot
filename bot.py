import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SEARCH_URLS = [
    {
        "store": "Total Cards",
        "url": "https://totalcards.net/search?type=product&q=dragon+ball+fusion+world"
    },
    {
        "store": "Chaos Cards",
        "url": "https://www.chaoscards.co.uk/search/dragon%20ball%20fusion%20world"
    },
    {
        "store": "Zatu Games",
        "url": "https://www.board-game.co.uk/search-results/?query=dragon%20ball%20fusion%20world"
    },
    {
        "store": "Magic Madhouse",
        "url": "https://magicmadhouse.co.uk/search?q=dragon%20ball%20fusion%20world"
    }
]

KEYWORDS = [
    "dragon ball",
    "dragonball",
    "fusion world",
    "dragon ball super"
]

BAD_WORDS = [
    "out of stock",
    "sold out",
    "unavailable"
]

GOOD_WORDS = [
    "add to cart",
    "add to basket",
    "in stock",
    "buy now",
    "pre-order",
    "preorder"
]


def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing Telegram secrets")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": False
        },
        timeout=20
    )

    print("Telegram response:", response.status_code)
    print(response.text)


def check_page(store, url):
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=25)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True).lower()

    has_dragon_ball = any(word in text for word in KEYWORDS)
    has_stock_word = any(word in text for word in GOOD_WORDS)
    has_bad_word = any(word in text for word in BAD_WORDS)

    print(f"Checked {store}: Dragon Ball={has_dragon_ball}, Stock word={has_stock_word}, Bad word={has_bad_word}")

    if has_dragon_ball and has_stock_word and not has_bad_word:
        return True

    return False


def main():
    print("Starting Dragon Ball stock check...")

    found = False

    for item in SEARCH_URLS:
        store = item["store"]
        url = item["url"]

        try:
            if check_page(store, url):
                found = True

                message = (
                    "🚨 DRAGON BALL STOCK FOUND\n\n"
                    f"🏪 Store: {store}\n"
                    f"🔗 Link: {url}\n\n"
                    f"⏰ Checked: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                )

                send_telegram(message)

        except Exception as e:
            print(f"Error checking {store}: {e}")

    if not found:
        print("No Dragon Ball stock found this run.")


if __name__ == "__main__":
    main()
