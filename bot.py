import os
import requests
from datetime import datetime

from priority import get_priority, priority_icon
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
            "disable_web_page_preview": False,
        },
        timeout=20,
    )

    print("Telegram response:", response.status_code)
    print(response.text)

    return response.status_code == 200


def main():
    print("Starting Dragon Ball UK stock check...")

    state = load_state()
    products = get_all_products()

    alerts_sent = 0
    in_stock_count = 0

    print(f"Products found: {len(products)}")

    for product in products:
        store = product["store"]
        name = product["name"]
        price = product["price"]
        url = product["url"]
        in_stock = product["in_stock"]

        if not in_stock:
            continue

        in_stock_count += 1

        if already_alerted(state, store, name, url):
            print(f"Already alerted: {store} - {name}")
            continue

        priority = get_priority(name)
        icon = priority_icon(priority)

        message = (
            f"{icon} DRAGON BALL RESTOCK {icon}\n\n"
            f"⭐ Priority: {priority}\n\n"
            f"🏪 Store: {store}\n"
            f"📦 Product: {name}\n"
            f"💷 Price: {price}\n"
            f"🔗 {url}\n\n"
            f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )

        if send_telegram(message):
            alerts_sent += 1
            mark_alerted(state, store, name, url)
            print(f"✅ Alert sent: {store} - {name}")

    save_state(state)

    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Stock check complete")
    print(f"Products scanned : {len(products)}")
    print(f"In stock         : {in_stock_count}")
    print(f"Alerts sent      : {alerts_sent}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


if __name__ == "__main__":
    main()