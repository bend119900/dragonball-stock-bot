from .total_cards import check_total_cards
from .travelling_man import check_travelling_man
from .japan2uk import check_japan2uk


def get_all_products():
    products = []

    products.extend(check_total_cards())
    products.extend(check_japan2uk())
    products.extend(check_travelling_man())

    return products