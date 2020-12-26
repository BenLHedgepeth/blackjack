
from random import shuffle
import sys
import functools

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
            if not player.chips:
                print(e)
                sys.exit()
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
                # import pdb; pdb.set_trace()
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
                Player has no winning hands to continue.
                You lost {player._bet} chips.
            """)
        else:
            # import pdb; pdb.set_trace()
            dealer_hand = blackjack_table.dealer.hands[0]
            while dealer_hand.value < 17:
                dealer_hand = blackjack_table.dealer.hit(
                    blackjack_table.card_stack
                )
            wins = 0
            for hand in player.hands:
                print(player.view_hand(
                    dealer_hand,
                    hand
                ))
                s = ''
                if dealer_hand.value > 21:
                    s +="Dealer hand is greater than 21...BUST."
                    s += "\nPlayer wins!"
                    wins += 1
                elif dealer_hand == hand:
                    s += "Hands have the same pip value...PUSH."
                    s += "\nNeither the player or dealer wins!"
                elif dealer_hand > hand:
                    s += "Dealer hand beats player hand...Dealer wins!"
                else:
                    s += "Player hand beats dealer hand...Player wins!"
                    wins += 1
                print(s)
            if wins == 1 and len(player.hands) == 2:
                player.chips += ((player._bet / 2) * 2)
            elif wins:
                player.chips += (player._bet * 2)
            else:
                print(f"Dealer wins the round.\nYou lost {player._bet} chips.")
            while True:
                play_again = input("Do you want to play again?\nY(es) or N(o)? ")
                if play_again not in ['Y', 'N']:
                    continue
                break
            if play_again == "Y":
                import pdb; pdb.set_trace()
                player._bet = 0
                dealer_cards = dealer_hand.cards
                if len(player.hands) == 2:
                    player_cards = player.hands[0].cards + player.hands[1].cards
                else:
                    player_cards = player.hands[0].cards
                all_dealt_cards = player_cards + dealer_cards
                player.hands = []
                blackjack_table.card_stack.extend(all_dealt_cards)
            else:
                sys.exit()



if __name__ == "__main__":
    main()
