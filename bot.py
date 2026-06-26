import os
import requests
from datetime import datetime

from stores import get_all_products
from tracker import load_state, save_state, already_alerted, mark_alerted

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


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


def main():
    print("Starting Dragon Ball UK stock check...")

    state = load_state()
    products = get_all_products()

    print(f"Products found: {len(products)}")

    for product in products:
        store = product["store"]
        name = product["name"]
        price = product["price"]
        url = product["url"]
        in_stock = product["in_stock"]

        if not in_stock:
            continue

        if already_alerted(state, store, name, url):
            print(f"Already alerted: {store} - {name}")
            continue

        message = (
            "🚨 DRAGON BALL PRODUCT FOUND\n\n"
            f"🏪 Store: {store}\n"
            f"📦 Product: {name}\n"
            f"💷 Price: {price}\n"
            f"🔗 Link: {url}\n\n"
            f"⏰ Checked: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )

        if send_telegram(message):
            mark_alerted(state, store, name, url)
            print(f"Alert sent: {store} - {name}")

    save_state(state)

    print("Stock check finished.")


if __name__ == "__main__":
    main()
