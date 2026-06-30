import requests

url = "https://travellingman.com/search/suggest.json?q=dragon%20ball%20fusion%20world&resources[type]=product"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=20,
)

data = response.json()

products = data["resources"]["results"]["products"]

print(f"Products found: {len(products)}")
print()

for product in products:
    print("Title     :", product["title"])
    print("Available :", product["available"])
    print("URL       :", product["url"])

    if "price" in product:
        print("Price     :", product["price"])

    print("-" * 40)