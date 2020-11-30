
from classes import Dealer, Player, Hand

class BlackjackTable:

    def __init__(self):
        self.dealer = Dealer()


def main():
    blackjack_table = BlackjackTable()
    player = Player()

    player_cards, dealer_cards = blackjack_table.dealer.deal(self.cards)
    if player_cards[0] == player_cards[1]:
        while True:
            try:
                double_down = input("Would you like to double_down? ").upper()
            except:
                pass
                continue
            else:
                if double_down == "Y":
                    player_cards = blackjack_table.dealer.deal(
                        self.cards, player_cards, True
                    )
                    break
                
