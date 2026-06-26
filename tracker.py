import json
import hashlib

STATE_FILE = "state.json"


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"alerts_sent": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def make_alert_id(store, product_name, product_url):
    raw = f"{store}|{product_name}|{product_url}"
    return hashlib.sha256(raw.encode()).hexdigest()


def already_alerted(state, store, product_name, product_url):
    alert_id = make_alert_id(store, product_name, product_url)
    return alert_id in state.get("alerts_sent", [])


def mark_alerted(state, store, product_name, product_url):
    alert_id = make_alert_id(store, product_name, product_url)

    if "alerts_sent" not in state:
        state["alerts_sent"] = []

    if alert_id not in state["alerts_sent"]:
        state["alerts_sent"].append(alert_id)
