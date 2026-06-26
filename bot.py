import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

KEYWORDS = [
    "dragon ball",
    "dragonball",
    "fusion world",
    "booster box",
    "booster pack",
    "dragon ball super",
]

STORES = [
    {
        "name": "Total Cards",
        "url": "https://totalcards.net/search?type=product&q=dragon+ball+fusion+world"
    },
    {
        "name": "Chaos Cards",
        "url": "https://www.chaoscards.co.uk/search/dragon%20ball%20fusion%20world"
    },
    {
        "name": "Zatu Games",
        "url": "https://www.board-game.co.uk/search-results/?query=dragon%20ball%20fusion%20world"
    },
    {
        "name": "Magic Madhouse",
        "url": "https://magicmadhouse.co.uk/search?q=dragon%20ball%20fusion%20world"
    },
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
            "disable_web_page_preview": True
        },
        timeout=20
    )

    print("Telegram response:", response.status_code)
    print(response.text)

def page_mentions_stock(text):
    text = text.lower()

    has_keyword = any(word in text for word in KEYWORDS)
    out_of_stock = any(phrase in text for phrase in [
        "out of stock",
        "sold out",
        "unavailable"
    ])

    add_to_cart = any(phrase in text for phrase in [
        "add to cart",
        "add to basket",
        "in stock",
        "buy now"
    ])

    return has_keyword and add_to_cart and not out_of_stock

def check_store(store):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(store["url"], headers=headers, timeout=25)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    if page_mentions_stock(text):
        return True

    return False

def main():
    found_anything = False

    for store in STORES:
        try:
            if check_store(store):
                found_anything = True
                message = (
                    "🚨 Dragon Ball Stock Alert!\n\n"
                    f"Store: {store['name']}\n"
                    f"Link: {store['url']}\n\n"
                    f"Checked: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                )
                send_telegram(message)
        except Exception as e:
            print(f"Error checking {store['name']}: {e}")

    if not found_anything:
        print("No stock found this run.")

if __name__ == "__main__":
    main()
