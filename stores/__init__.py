from .total_cards import check_total_cards
from .travelling_man import check_travelling_man
from .japan2uk import check_japan2uk
from .hammerhead_tcg import check_hammerhead_tcg
from .sports_cards_direct import check_sports_cards_direct
from .the_card_vault import check_the_card_vault
from .rules_of_play import check_rules_of_play
from .the_vault_tcg import check_the_vault_tcg
from .wiggys_collectables import check_wiggys_collectables
from .ultimate_tcg import check_ultimate_tcg
from .the_card_cloud import check_the_card_cloud

def get_all_products():
    products = []

    products.extend(check_total_cards())
    products.extend(check_japan2uk())
    products.extend(check_travelling_man())
    products.extend(check_sports_cards_direct())
    products.extend(check_hammerhead_tcg())
    products.extend(check_the_card_vault())
    products.extend(check_rules_of_play())
    products.extend(check_the_vault_tcg())
    products.extend(check_wiggys_collectables())
    products.extend(check_ultimate_tcg())
    products.extend(check_the_card_cloud())

    return products