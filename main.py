
import logging

from classes import Dealer, Player, Hand
from utils import cards

logging.basicConfig(level=logging.INFO)

class BlackjackTable:

    def __init__(self):
        self.card_stack = cards()
        self.dealer = Dealer()
        self.players = [self.dealer]
        self.i = 0


    def __iter__(self):
        return self

    def __next__(self):

        if self.i < len(self.players):
            person = self.players[self.i]
            self.i += 1
            return person
        else:
            raise StopIteration()


def main():
    blackjack_table = BlackjackTable()
    player = Player()
    blackjack_table.players.append(player)
    while True:
        shuffle(blackjack_table.card_stack)
        try:
            player.bet()
        except ValueError as e:
            print(e)
        for i in range(2):
            for player in blackjack_table:
                if i == 1:
                    cards = []
                dealt_card = blackjack_table.dealer.deal(self.card_stack)
                cards.append(card)
                if i == 2 and str(player) == "Player":
                    player.hands.append(Hand(cards))
                else:
                    player.hand = Hand(cards)
        break
    logging.info("Hands have been dealt to both the Player and the Dealer")
    hands, position = player.check_hand()
    while position != "STAND":
        if position == "DOUBLE_DOWN":
            player.bet()
            dealt_card = self.dealer.deal()
            player.hands[0].cards.append(dealt_card)
            break
        elif position == "SPLIT":
            for hand in hands:
                dealt_card = self.dealer.deal(self.card_stack)
                hand.cards.append(dealt_card)
            hands, position = player.check_hand()
