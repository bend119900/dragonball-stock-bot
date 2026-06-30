import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def test_store(name, base_url):
    print("=" * 60)
    print(f"Testing: {name}")
    print("=" * 60)

    tests = [
        "/products.json?limit=5",
        "/search/suggest.json?q=dragon%20ball&resources[type]=product",
        "/search?q=dragon+ball",
    ]

    for path in tests:
        url = base_url.rstrip("/") + path

        try:
            response = requests.get(url, headers=HEADERS, timeout=15)

            print(f"{response.status_code:3}  {path}")

        except Exception as e:
            print(f"ERR  {path}")
            print(e)

    print()