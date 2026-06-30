from store_tester import test_store

stores = [
    ("Travelling Man", "https://travellingman.com"),
    ("Total Cards", "https://totalcards.net"),
    ("Magic Madhouse", "https://magicmadhouse.co.uk"),
    ("Card Vault", "https://www.cardvault.co.uk"),
    ("Patriot Games", "https://patriotgames.uk"),
    ("The Brotherhood Games", "https://thebrotherhoodgames.co.uk"),
]

for name, url in stores:
    test_store(name, url)