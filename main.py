
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
        z = 0
        while z < len(player.hands):
            position = player.check_hand(
                blackjack_table.dealer.hands[0], player.hands[z]
            )
            if position == "SPLIT":
                player_hands = player.hands.copy()
                for i, hand in enumerate(player_hands):
                    dealt_card = blackjack_table.dealer.deal_card(
                        blackjack_table.card_stack
                    )
                    player.hands[i].cards.append(dealt_card)
                continue
            while position != "BUST":
                import pdb; pdb.set_trace()
                if position == "HIT" or position == "DOUBLE DOWN":
                    dealt_card = blackjack_table.dealer.deal_card(
                        blackjack_table.card_stack
                    )
                    player.hands[z].cards.append(dealt_card)
                    position = player.check_hand(
                        blackjack_table.dealer.hands[0], player.hands[z]
                    )
                    continue
                elif position == "STAND":
                    break
            if position != "BUST":
                z += 1
                pass
            else:
                del player.hands[z]
                z += 1
                break
            continue
        # import pdb; pdb.set_trace()
        if not player.hands:
            print(f"""
                Dealer wins the round.
                You lost {player._bet} chips.
            """)
            player._bet = 0
            continue
        else:
            import pdb; pdb.set_trace()
            dealer_hand = blackjack_table.dealer.hands[0]
            if all(h.value < dealer_hand.value for h in player.hands):
                print("You lost!")
                player._bet = 0
                while True:
                    try:
                        play_again = input("Do you want to play again?\nY(es) or N(o)? ")
                    except ValueError:
                        continue
                    if play_again is None:
                        continue
                    break
                    if play_again == "Y":
                        pass

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
                    player.chips += player._bet
                else:
                    wins = len(list(filter(
                        lambda h: h > dealer_hand, player.hands
                    )))
                    if wins == 1 and len(player.hands) == 2:
                        player.chips += ((player._bet / 2) * 2)
                    elif wins:
                        player.chips += (player._bet * 2)
                    else:
                        print(f"""
                            Dealer wins the round.
                            You lost {player._bet} chips.
                        """)
                        player._bet = 0
                        continue
                player._bet = 0

        all_dealt_hands = blackjack_table.dealer.hands + player_hands

if __name__ == "__main__":
    main()
