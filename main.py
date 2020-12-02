

from classes import Dealer, Player, Hand
from utils import cards

class BlackjackTable:

    def __init__(self):
        self.cards = cards()
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
    while True:
        for i in range(2):
            for player in blackjack_table:
                if i == 1:
                    cards = []
                dealt_card = blackjack_table.dealer.deal(self.cards)
                cards.append(card)
                if i == 2:
                    hand = Hand(cards)
                    player.hands.append(hand)

    player_hand_status = person.check_hand(hand)
