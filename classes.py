
class Dealer:

    def __init__(self, chips=50000):
        self.chips = 50000
        self.name = "Dealer"

    def shuffle(self):
        pass


    def deal(self, cards, player_cards=[]):
        if not player_cards:
            player_cards = [cards.pop(0) for _ in range(2)]
            player_cards, dealer_cards = cards[0: len(dealt_cards) + 1: 2], cards[1: len(dealt_cards) + 1: 2]
            return player_cards, dealer_cards
        elif player_cards and double:
            new_cards = [cards.pop(0) for _ in range(2)]
            return zip(player_cards, new_cards)
        elif player_cards and not double:
            new_card = cards.pop()
            # return player_cards.extend(new_card)


class Player:

    def __init__(self):
        self.chips = 0
        self.hands = []
        self.name = 'Player'

    def bet(self):
        try:
            bet_placed = int(input("Please place your bet: "))
            if not bet_placed:
                raise ValueError("Cannot accept the bet placed!")
        except ValueError:
            raise
        else:
            return bet_placed

    def check_hand(self):
        cards = self.hands[0].cards
        if len(self.hands) == 1 and cards[0] == cards[1]:
            while True:
                split_cards = input("Do you want to split your cards? ").upper()
                if not split_cards or split_cards not in ["Y", "N"]:
                    print("Cannot accept card play...")
                    continue
                else:
                    break
            if split_cards == "Y":
                return [[card, ] for card in cards], "split"
        positon = self.hit_or_stand()
        return position

    def hit_or_stand(self):
        if self.hands[0].value < 21:
            while True:
                position = input("Would you like to hit or stand")
                if not position or position not in ["STAND", "HIT"]:
                    print("Cannot accept blackjack play... ")
                    continue
                else:
                    return self.hands[0], position



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

    def __len__(self):
        return len(self.cards)

    def __eq__(self, other):
        return self.value == other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value
