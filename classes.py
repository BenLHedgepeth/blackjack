
from exceptions import LowChipsException

class Dealer:

    def __init__(self, chips=50000):
        self.chips = 50000
        self.name = "Dealer"
        self.hands = []

    def deal(self, cards):
        card = cards.pop(0)
        return card

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return


class Player:

    def __init__(self):
        self.chip_stack = 0
        self.bets_made = 0
        self.hands = []
        self.name = 'Player'

    def __str__(self):
        return f"{self.name}"

    def bet(self):
        existing_bet = getattr(self, 'bets_made')
        if existing_bet and self.chip_stack:
            self.chip_stack -= existing_bet
            if self.chip_stack < 0:
                self.chip_stack += existing_bet
                raise LowChipsException("Your bet exceeds your current chip standing!")
            self.bets_made += self.bets_made
        elif not existing_bet and self.chip_stack:
            '''Represents the inital bet before cards are dealt'''
            while True:
                try:
                    bet_placed = abs(int(input("Please place your bet: ")))
                    if not bet_placed:
                        print("Cannot accept the bet placed!")
                        continue
                except ValueError:
                    print("Cannot accept the bet placed!")
                    continue
                else:
                    self.chip_stack -= bet_placed
                    self.bets_made += bet_placed
                    return
        else:
            raise LowChipsException("You have no chips remaining!")

    def check_hand(self, dealer):
        hand_values = map(lambda hand: hand.value, self.hands)
        for i, hand in enumerate(self.hands):
            print(f"{str(self.hands[i])}\n" + '-' * len(str(self.hands[i])) + "\n" + f"Total hand: {hand.value}")

        if (len(self.hands) == 1 and
        all(card.pip == 11 for card in self.hands[0].cards) or
        all(card.pip == 8 for card in self.hands[0].cards)):
            print("Split the cards...")
            self.bet()
            cards, position = self.split_hand()
            return (cards, position)

        while True:
            position = input("Which play would you like to perform? ").upper()
            if position == "SPLIT":
                if len(self.hands) == 2:
                    print("Can only split your hand one time!")
                else:
                    try:
                        self.bet()
                        hands, position = self.split_hand()
                    except ValueError:
                        print("""
                            The cards dealt to you don't have the same pip value.
                            You can only 'HIT', 'STAND', or 'DOUBLE DOWN'.
                        """)
                    except LowChipsException as e:
                        print(e)
                    else:
                        return (hands, "SPLIT")
            elif position == "DOUBLE DOWN":
                try:
                    self.bet()
                except LowChipsException as e:
                    print(e)
                else:
                    hands = self.hands
                    return (hands, "DOUBLE_DOWN")
            elif position == "STAND":
                hands, position = self.stand()
            else:
                pass

    def split_hand(self):
        cards = self.hands[0].cards
        if cards[0] != cards[1]:
            raise ValueError
        hands = []
        for card in cards:
            hands.append(Hand([card]))
        self.hands = hands
        return (self.hands, "SPLIT")

    # def stand(self):
    #
    #     ace_exists = list(filter(lambda hand: any(hasattr(card, 'face_card') and card.face_card == 'Ace' for card in hand.cards), self.hands))
    #
    #     if ace_exists:
    #             try:
    #                 ace_value = abs(int(input("Do you want your 'Ace(s)' to be worth 1 or 11 pips")))
    #             except ValueError:
    #                 print("Invalid pip value for your 'Ace(s)'")
    #             else:
    #                 for hand in self.hands:
    #                     for card in hand.cards:
    #                         if hasattr(card, 'face_card') and card.face_card == 'Ace':
    #                             card.pip = ace_value
    #                 hands = self.hands
    #     return (hands, "STAND")






class Card:

    def __init__(self, pip, suit, *args, **kwargs):
        self.pip = pip
        self.suit = suit
        if kwargs.get('face_card', None):
            self.face_card = kwargs['face_card']

    def __repr__(self):
        if hasattr(self, "face_card"):
            return f"{self.face_card} of {self.suit}"
        return f"{self.pip} of {self.suit}"

    def __eq__(self, other):
        return self.pip == other.pip


class Hand:

    def __init__(self, cards):
        self.cards = cards
        self.value = sum([card.pip for card in self.cards])

    def __str__(self):
        return "".join([str(card) + "\n" for card in self.cards])

    def __repr__(self):
        return "".join([f"{card}, " if i == 0 else f"{card}" for i, card in enumerate(self.cards)])

    def __len__(self):
        return len(self.cards)

    def __eq__(self, other):
        return self.value == other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value
