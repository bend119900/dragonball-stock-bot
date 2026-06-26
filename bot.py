import os
import json
import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
STATE_FILE = "state.json"

STORES = [
    {
        "store": "Total Cards",
        "url": "https://totalcards.net/search?type=product&q=dragon+ball+fusion+world"
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

STOCK_WORDS = [
    "add to cart",
    "add to basket",
    "buy now",
    "pre-order",
    "preorder",
    "in stock"
]

OUT_OF_STOCK_WORDS = [
    "out of stock",
    "sold out",
    "unavailable"
]


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"alerts_sent": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing Telegram secrets")
        return False

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

    return response.status_code == 200


def make_alert_id(store, url):
    raw = f"{store}|{url}"
    return hashlib.sha256(raw.encode()).hexdigest()


def page_has_dragon_ball_stock(text):
    text = text.lower()

    has_keyword = any(word in text for word in KEYWORDS)
    has_stock = any(word in text for word in STOCK_WORDS)
    out_of_stock = any(word in text for word in OUT_OF_STOCK_WORDS)

    return has_keyword and has_stock and not out_of_stock


def check_store(store):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print(f"Checking {store['store']}...")

    response = requests.get(store["url"], headers=headers, timeout=25)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    found = page_has_dragon_ball_stock(text)

    print(f"{store['store']} result: {found}")

    return found


def main():
    print("Starting Dragon Ball UK stock check...")

    state = load_state()
    alerts_sent = state.get("alerts_sent", [])

    for store in STORES:
        try:
            found = check_store(store)

            if found:
                alert_id = make_alert_id(store["store"], store["url"])

                if alert_id not in alerts_sent:
                    message = (
                        "🚨 DRAGON BALL STOCK FOUND\n\n"
                        f"🏪 Store: {store['store']}\n"
                        f"🔗 Link: {store['url']}\n\n"
                        f"⏰ Checked: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                    )

                    if send_telegram(message):
                        alerts_sent.append(alert_id)
                        print(f"Alert sent for {store['store']}")
                else:
                    print(f"Already alerted for {store['store']}, skipping.")

        except Exception as e:
            print(f"Error checking {store['store']}: {e}")

    state["alerts_sent"] = alerts_sent
    save_state(state)

    print("Stock check finished.")


if __name__ == "__main__":
    main()
