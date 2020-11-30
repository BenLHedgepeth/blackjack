
class Dealer:
    def __init__(self):
        self.name = Dealer
        self.hand = None

    def shuffle(self):
        pass

    def deal(self, cards, player):
        import pdb; pdb.set_trace()
        if player and not getattr(player.hand, 'cards', None):
            cards = [cards.pop(0) for _ in range(4)]
            player_cards, dealer_cards = cards[0:len(cards) + 1:2], cards[1:len(cards) + 1:2]
            return player_cards, dealer_cards


class Player:
    def __init__(self):
        self.name = 'player'
        self.hand = None

    def bet(self):
        pass


class Card:
    def __init__(self, pip_value, suit, *args, **kwargs):
        self.pip_value = pip_value
        self.suit = suit
        if kwargs.get("face_card", None):
            self.face_card = kwargs["face_card"]

    def __repr__(self):
        if hasattr(self, "face_card"):
            return f"{getattr(self, 'face_card')} of {self.suit}"
        return f"{self.pip_value} of {self.suit}"

    def __eq__(self, other):
        return self.pip_value == other.pip_value


class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.value = sum([card.pip_value for card in self.cards])

    def __len__(self):
        return len(self.cards)

    def __eq__(self, other):
        return self.value == other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value
