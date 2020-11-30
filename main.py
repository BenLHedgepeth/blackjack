
from classes import Dealer, Player

class BlackjackTable:

    def __init__(self):
        self.dealer = Dealer()


def main():
    blackjack_table = BlackjackTable()
    player = Player()
    
    player_cards, dealer_cards = blackjack_table.dealer.deal(self.cards, player)
    if len(player_cards) == 4:
        card_set1, card_set2 = player_cards[0:2:2], player_cards[1:3:2]
    else:
        card_set1 = player_cards
