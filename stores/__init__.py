from .total_cards import check_total_cards
from .travelling_man import check_travelling_man
from .japan2uk import check_japan2uk
from .hammerhead_tcg import check_hammerhead_tcg
from .sports_cards_direct import check_sports_cards_direct
from .the_card_vault import check_the_card_vault

def get_all_products():
    products = []

    products.extend(check_total_cards())
    products.extend(check_japan2uk())
    products.extend(check_travelling_man())
    products.extend(check_sports_cards_direct())
    products.extend(check_hammerhead_tcg())
    products.extend(check_the_card_vault())

    return products