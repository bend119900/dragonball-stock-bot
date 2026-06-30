import requests

url = "https://www.cardvault.co.uk/search/suggest.json?q=dragon%20ball%20fusion%20world&resources[type]=product"

response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)

print("Status:", response.status_code)
print(response.text[:1500])