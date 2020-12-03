
class Dealer:

    def __init__(self, chips=50000):
        self.chips = 50000
        self.name = "Dealer"

    def deal(self, cards):
        card = cards.pop(0)
        return card


class Player:

    def __init__(self):
        self.chips = 0
        self.hands = []
        self.name = 'Player'

    def bet(self):
        if not self.chips:
            raise ValueError("You have no more chips...Goodbye!")
        while True:
            try:
                bet_placed = abs(int(input("Please place your bet: ")))
                if not bet_placed:
                    print("Cannot accept the bet placed!")
            except ValueError:
                print("Cannot accept the bet placed!")
            break
        self.chips -= bet_placed
        return bet_placed

    def check_initial_hand(self, dealer):
        cards = self.hands[0].cards

        while True:
            position = input("Which play would you like to perform? ").upper()
            if position == "SPLIT":
                try:
                    hands, pos = self.split_hand()
                except ValueError:
                    print("""
                        The cards dealt to you don't have the same pip value.
                        You can only 'HIT', 'STAND', or 'DOUBLE DOWN'.
                    """)
                else:
                    return hands, pos
            elif position == "DOUBLE DOWN":
                pass

        # positon = self.hit_or_stand()
        # return position

    def split_hand(self):
        import pdb; pdb.set_trace()
        cards = self.hands[0].cards
        try:
            hand1, hand2 = [[Hand([card]), ] for card in cards if cards[0] == cards[1]]
        except ValueError:
            raise
        return ([hand1, hand2], "SPLIT")

    def hit_or_stand(self):
        if len(self.hands) == 1 and self.hands[0].value < 21:
            while True:
                position = input("Would you like to hit or stand")
                if not position or position not in ["STAND", "HIT"]:
                    print("Cannot accept blackjack play... ")
                    continue
                else:
                    return self.hands, position



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
        return " ".join([str(card) + '/n' for card in self.cards])

    def __len__(self):
        return len(self.cards)

    def __eq__(self, other):
        return self.value == other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value
