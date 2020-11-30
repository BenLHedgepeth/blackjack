
class Dealer:

    def __init__(self):
        self.name = Dealer
        self.hand = None

    def shuffle(self):
        pass

    def deal(self, cards, player_cards=[], double=False):
        import pdb; pdb.set_trace()
        if not player_cards:
            cards = [cards.pop(0) for _ in range(4)]
            player_cards, dealer_cards = cards[0:len(cards) + 1:2], cards[1:len(cards) + 1:2]
            return player_cards, dealer_cards
        elif player_cards and double:
            new_cards = [cards.pop(0) for _ in range(2)]
            return zip(player_cards, new_cards)
        elif player_cards and not double:
            new_card = cards.pop()
            return card



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
            return f"{self.face_card} of {self.suit}"
        return f"{self.pip_value} of {self.suit}"

    def __eq__(self, other):
        return self.pip_value == other.pip_value


class Hand:

    def __init__(self, cards):
        self.cards = cards
        self.value = sum([card.pip_value for card in self.cards])

    @property
    def _cards:
        return []

    def __len__(self):
        return len(self.cards)

    def __eq__(self, other):
        return self.value == other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value
