
from exceptions import LowChipsException

class Dealer:

    def __init__(self, chips=50000):
        self.chips = 50000
        self.name = "Dealer"

    def deal(self, cards):
        card = cards.pop(0)
        return card


class Player:

    def __init__(self):
        self.chip_stack = 0
        self.bets_made = 0
        self.hands = []
        self.name = 'Player'

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
                except ValueError:
                    print("Cannot accept the bet placed!")
                else:
                    self.chip_stack -= bet_placed
                    self.bets_made += bet_placed
                    return
        else:
            raise LowChipsException("You have no chips remaining!")

    def check_hand(self, dealer):
        my_cards = self.hands[0].cards

        while True:
            position = input("Which play would you like to perform? ").upper()
            if position == "SPLIT":
                try:
                    self.bet()
                    hands, pos = self.split_hand()
                except ValueError:
                    print("""
                        The cards dealt to you don't have the same pip value.
                        You can only 'HIT', 'STAND', or 'DOUBLE DOWN'.
                    """)
                except LowChipsException as e:
                    print(e)
                else:
                    return hands, pos
            elif position == "DOUBLE DOWN":
                try:
                    self.bet()
                except LowChipsException as e:
                    print(e)
                else:
                    return (self.hands, "DOUBLE_DOWN")

        # positon = self.hit_or_stand()
        # return position

    def split_hand(self):
        cards = self.hands[0].cards
        if cards[0] != cards[1]:
            raise ValueError
        hands = []
        for card in cards:
            hands.append(Hand([card]))
        self.hands = hands
        return (self.hands, "SPLIT")

    def hit_or_stand(self):
        pass



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
        return " ".join([str(card) for card in self.cards])

    def __repr__(self):
        return " ".join([str(card) + '/n' for card in self.cards])

    def __len__(self):
        return len(self.cards)

    def __eq__(self, other):
        return self.value == other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value
