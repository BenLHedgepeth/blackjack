
from random import shuffle
import logging
import itertools

from classes import Dealer, Player, Hand
from utils import cards, collect_chips

from exceptions import BettingError
logging.basicConfig(level=logging.INFO)

class BlackjackTable:

    def __init__(self):
        self.card_stack = cards()
        self.dealer = Dealer()
        self.player = None


def main():
    blackjack_table = BlackjackTable()
    player = Player()
    blackjack_table.player = player
    print("Welcome to the Blackjack Table! Let's get started!")
    player.chips = collect_chips()
    while True:
        shuffle(blackjack_table.card_stack)
        try:
            player.bet()
        except ValueError as e:
            print(e)
            continue
        except BettingError as e:
            print(e)
            continue
        else:
            dealer_hand, player_hand = blackjack_table.dealer.deal_hands(
                blackjack_table.card_stack,
                player
            )
            logging.info(
                "Hands have been dealt to both the Player and the Dealer."
            )
        player_hands = player.hands.copy()
        i = 0
        while i < len(player.hands):
            '''See Note (1).'''
            position = player.check_hand(blackjack_table.dealer.hands[0], player.hands[i])
            while position != "BUST":
                if position == "SPLIT":
                    for i, hand in enumerate(player.hands):
                        dealt_card = blackjack_table.deal_card(
                            blackjack_table.card_stack
                        )
                        player.hands[i].cards.append(deal_card)
                        i += 1
                    i = 0
                    break
                elif position == "HIT" or position == "DOUBLE DOWN":
                    dealt_card = blackjack_table.dealer.deal_card(
                        blackjack_table.card_stack
                    )
                    player.hands[i].cards.append(dealt_card)
                    position = player.check_hand(blackjack_table.dealer.hands[0], player.hands[i])
                    continue
                    if position == "DOUBLE DOWN":
                        i += 1
                        break
                elif position == "STAND":
                    i += 1
                    break
            del player_hands[i]
            i += 1
            continue
        if not player_hands:
            print("HERE")
    # if all(hand.value > 21 for hand in final_hands):
    #     print(f"""
    #         Dealer wins the round.
    #         You lost {player._bet} chips.
    #     """)
    #     all_dealt_hands = blackjack_table.dealer.hands + final_hands
    #     for hand in all_dealt_hands:
    #
    #         for card in hand.cards:
    #
    #     blackjack_table.dealer.chips += player._bet
    #     player._bet = 0
    # print("You win")

'''(1): The initial hand was being passed to player.check_hand() on
two different lines in the source code when implementing a for loop.
If a player received a hand that could not be split, the second call
to the initial hand would occur when evaluating to hit, stand, or double down.

If the player is unable to split their cards, player.check_hand() was being
called on the same hand twice
'''

if __name__ == "__main__":
    main()
