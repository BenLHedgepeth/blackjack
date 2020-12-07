
from random import shuffle
import logging
import itertools

from classes import Dealer, Player, Hand
from utils import cards, collect_chips

from exceptions import LowChipsException
logging.basicConfig(level=logging.INFO)

class BlackjackTable:

    def __init__(self):
        self.card_stack = cards()
        self.dealer = Dealer()
        self.players = [self.dealer]

    def __iter__(self):
        self.i = 0
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
    blackjack_table.players.insert(0, player)
    player.chip_stack = collect_chips()
    while True:
        shuffle(blackjack_table.card_stack)
        try:
            player.bet()
        except ValueError as e:
            print(e)
            continue
        except LowChipsException:
            print("No chips!")
            continue
        else:
            dealt_cards = {'Player': [], 'Dealer': []}
            for i in range(2):
                for person in blackjack_table:
                    dealt_card = blackjack_table.dealer.deal(blackjack_table.card_stack)
                    dealt_cards[f"{person}"].append(dealt_card)
                    if i == 1:
                        person.hands.append(Hand(dealt_cards[f"{person}"]))


        logging.info("Hands have been dealt to both the Player and the Dealer")
        hands, position = player.check_hand(blackjack_table.dealer)

        while position != "STAND":
            if position == "DOUBLE_DOWN":
                dealt_card = blackjack_table.dealer.deal(blackjack_table.card_stack)
                player.hands[0].cards.append(dealt_card)
                break
            elif position == "SPLIT":
                for i, hand in enumerate(hands):
                    dealt_card = blackjack_table.dealer.deal(blackjack_table.card_stack)
                    player.hands[i].cards.append(dealt_card)
                hands, position = player.check_hand(blackjack_table.dealer)
            elif posiiton == "HIT":
                dealt_card = blackjack_table.dealer.deal(blackjack_table.card_stack)
                hands, position = player.check_hand(blackjack_table.dealer)
            else:
                break

if __name__ == "__main__":
    main()
