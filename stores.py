from stores.total_cards import check_total_cards


def get_all_products():
    products = []

    try:
        products.extend(check_total_cards())
    except Exception as e:
        print(f"Total Cards error: {e}")

    return products
