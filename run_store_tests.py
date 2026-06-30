from store_tester import test_store

stores = [
    ("Japan2UK", "https://www.japan2uk.com"),
    ("Unicorn Cards", "https://www.unicorncards.co.uk"),
    ("The Card Vault UK", "https://thecardvault.co.uk"),
    ("Big Orbit Cards", "https://www.bigorbitcards.co.uk"),
    ("Travelling Man", "https://travellingman.com"),
    ("Total Cards", "https://totalcards.net"),
    ("Magic Madhouse", "https://magicmadhouse.co.uk"),
    ("Card Vault", "https://www.cardvault.co.uk"),
    ("Patriot Games", "https://patriotgames.uk"),
    ("The Brotherhood Games", "https://thebrotherhoodgames.co.uk"),
]

for name, url in stores:
    test_store(name, url)