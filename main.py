
from random import shuffle
import logging
import itertools

from classes import Dealer, Player, Hand
from utils import cards, collect_chips

from exceptions import BettingError


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
            # import pdb; pdb.set_trace()
            blackjack_table.dealer.deal_hands(
                blackjack_table.card_stack,
                player
            )
        player_hands = player.hands.copy()
        i = 0
        while i < len(player.hands):
            position = player.check_hand(
                blackjack_table.dealer.hands[0], player.hands[i]
            )
            while position != "BUST":
                if position == "SPLIT":
                    for i, hand in enumerate(player_hands):
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
                    i += 1
                    break
            if position != "BUST":
                pass
            else:
                del player.hands[i]
                i += 1
        # import pdb; pdb.set_trace()
        if not player.hands:
            print(f"""
                Dealer wins the round.
                You lost {player._bet} chips.
            """)
            player._bet = 0
            continue
        else:
            # import pdb; pdb.set_trace()
            dealer_hand = blackjack_table.dealer.hands[0]
            while dealer_hand.value < 17:
                dealer_hand = blackjack_table.dealer.hit(
                    blackjack_table.card_stack
                )
            if dealer_hand.value > 21:
                print("You win")
                player.chips += (player._bet * 2)
                player._bet = 0
                play_again = input("Do you want to play another round? ")
                if not play_again:
                    pass
            else:
                if all(h.value == dealer_hand.value for h in player.hands):
                    self.chips += player._bet
                else:
                    wins = len(list(filter(
                        lambda h: h > dealer_hand, player.hands
                    )))
                    if len(wins) == 1 and len(player.hands) == 2:
                        self.chips += ((player._bet / 2) * 2)
                    else:
                        self.chips += (player._bet * 2)
                player._bet = 0

        all_dealt_hands = blackjack_table.dealer.hands + player_hands


if __name__ == "__main__":
    main()
