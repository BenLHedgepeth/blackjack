
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
            blackjack_table.dealer.deal_hands(
                blackjack_table.card_stack,
                player
            )
        player_hands = player.hands.copy()
        i = 0
        while i < len(player.hands):
            '''See Note (1).'''
            position = player.check_hand(
                blackjack_table.dealer.hands[0], player.hands[i]
            )
            # import pdb; pdb.set_trace()
            while position != "BUST":
                if position == "SPLIT":
                    for i, hand in enumerate(player.hands):
                        dealt_card = blackjack_table.dealer.deal_card(
                            blackjack_table.card_stack
                        )
                        player.hands[i].cards.append(dealt_card)
                        i += 1
                    i = 0
                    break
                elif position == "HIT" or position == "DOUBLE DOWN":
                    dealt_card = blackjack_table.dealer.deal_card(
                        blackjack_table.card_stack
                    )
                    player.hands[i].cards.append(dealt_card)
                    if position == "DOUBLE DOWN":
                        i += 1
                        break
                    position = player.check_hand(
                        blackjack_table.dealer.hands[0], player.hands[i]
                    )
                    continue
                elif position == "STAND":
                    import pdb; pdb.set_trace()
                    i += 1
                    break
            if position != "BUST":
                pass
            else:
                del player_hands[i]
                i += 1
        if not player_hands:
            print("HERE")
        import pdb; pdb.set_trace()
        print("PLAYER HANDS EXIST")
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


if __name__ == "__main__":
    main()
