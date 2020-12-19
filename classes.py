
from exceptions import BettingError, HandSplitError


class Card:
    def __init__(self, pip, suit, *args, **kwargs):
        self.pip = pip
        self.suit = suit
        if kwargs and 'face_card' in kwargs:
            self.face_card = kwargs['face_card']

    def __str__(self):
        if hasattr(self, 'face_card'):
            return f"{self.face_card} of {self.suit}"
        return f"{self.pip} of {self.suit}"

    def __repr__(self):
        props = f"({self.pip}, {self.suit}"
        if not hasattr(self, 'face_card'):
            return f"{self.__class__.__name__}{props})"
        props += f", face_card={self.face_card})"
        return f"{self.__class__.__name__}{props}"


    def __eq__(self, other):
        return self.pip == other.pip



class Hand:
    def __init__(self, cards):
        self.cards = cards
        self._value = sum(card.pip for card in cards)

    def __str__(self):
        return "".join(
            [f"{str(card)}, " if i == 0 else f"{str(card)}"
            for i, card in enumerate(self.cards)]
        )

    def __repr__(self):
        card_string = '(['
        for i, card in enumerate(self.cards):
            if i != len(self.cards) - 1:
                card_string += f"Card({card.pip}, {card.suit}), "
            else:
                card_string += f"Card({card.pip}, {card.suit})"
        card_string += '])'

        return f"{self.__class__.__name__}{card_string}"

    def __len__(self):
        return len(self.cards)

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    @property
    def value(self):
        return sum(card.pip for card in self.cards)

    @value.setter
    def value(self, value):
        self._value = value


    @property
    def soft(self):
        return any(
            hasattr(card, 'face_card') and
            card.face_card == "Ace" for card in self.cards
        )


class Dealer:
    def __init__(self):
        self.name = "Dealer"
        self.hands = []

    def __str__(self):
        return self.name

    def deal_hands(self, cards, player):

        dealt_cards = {f"{player}": [], f"{self}": []}
        for i in range(2):
            for person in (player, self):
                dealt_card = self.deal_card(cards)
                dealt_cards[f"{person}"].append(dealt_card)
                if i == 1:
                    hand = Hand(dealt_cards[f"{person}"])
                    person.hands.append(hand)
        return [self.hands[0], player.hands[0]]

    def deal_card(self, cards):
        card = cards.pop(0)
        return card


class Player:

    def __init__(self):
        self.name = "Player"
        self.hands = []
        self.chips = 0
        self._bet = 0

    def __str__(self):
        return self.name

    def bet(self):

        if not self.chips:
            raise BettingError("You have no chips remaining...")
        if self._bet:
            self.chips -= self._bet
            if (self.chips < 0):
                self.chips += self._bet
                raise BettingError(
                    "Your bet cannot be fulfilled due to inadequate chips."
                )
            self._bet += self._bet
        else:
            while True:
                try:
                    bet_placed = abs(int(input("Place your bet: ")))
                except ValueError:
                    print("Cannot accept the subject bet. Try again.")
                    continue
                else:
                    if not bet_placed:
                        print("Cannot accept the subject bet. Try again.")
                    else:
                        self.chips -= bet_placed
                        self._bet += bet_placed
                        break

    def split_hand(self, hand):

        cards = hand.cards
        if len(self.hands) > 1:
            raise ValueError("Cannot split hands past your initial hand.")
        elif len(cards) > 3:
            raise ValueError("Cannot split a hand that you have doubled down on.")
        elif cards[0] != cards[1]:
            raise HandSplitError(
                "Cannot split any cards where their pip values aren't equal."
            )
        hands = [Hand([card, ]) for card in cards]
        self.hands = hands
        return self.hands

    def check_hand(self, dealer_hand, player_hand):

        print(f"""
            Chips: {self.chips} - Bet: {self._bet} chips - Hand Score: {player_hand.value}\n
        """)
        str_hand1 = list(map(lambda x: len(str(x)), player_hand.cards))
        str_hand2 = list(map(lambda x: len(str(x)), dealer_hand.cards))
        max_str_length = max(str_hand1 + str_hand2) + 5

        card_strings = []
        for hand in (player_hand, dealer_hand):
            if hand is player_hand:
                string = f"\t\t\t{('-' * max_str_length)}\n\t\t\tPlayer\n\t\t\t{'=' *  max_str_length}"
            else:
                string = f"\t\t\t{('-' * max_str_length)}\n\t\t\tDealer\n\t\t\t{'=' *  max_str_length}"
            for i, card in enumerate(hand.cards):
                string += f"\n\t\t\t"
                if i == 1 and hand is dealer_hand:
                    string += f"\n\t\t\t{'Down card'.center(max_str_length)}"
                else:
                    string += f"\n\t\t\t{str(card).center(max_str_length)}"
            string += f"\n\t\t\t{'-' * max_str_length}\n"
            card_strings.append(string)

        card_strings = ''.join(card_strings)
        print(card_strings)

        while True:
            # import pdb; pdb.set_trace()
            play = input("How do you want to play your hand? ").upper()
            if play not in ['DOUBLE DOWN', "SPLIT", "HIT", "STAND"]:
                print("That play is not possible. Try another play.")
                continue
            if play == "SPLIT" or play == "DOUBLE DOWN":
                try:
                    self.bet()
                except BettingError as e:
                    print(e)
                    continue
                else:
                    if play == "SPLIT":
                        try:
                            hands = self.split_hand(player_hand)
                            self.hands = hands
                            return self.hands, "SPLIT"
                        except HandSplitError as e:
                            print(e)
                            self._bet /= 2
                            self.chips += self._bet
                            continue
                    elif play == "DOUBLE DOWN":
                        try:
                            hands = self.double_down(player_hand)
                        except ValueError as e:
                            print(e)
                            self._bet /= 2
                            self.chips += self._bet
                            continue
                        return play
            elif play == "HIT":
                position = self.hit(player_hand)
                return position
            return "STAND"

    def double_down(self, hand):
        if len(hand.cards) >= 3:
            raise ValueError(
                "You can only double down with two cards in a hand."
            )
        return "DOUBLE DOWN"

    def hit(self, hand):
        if hand.soft:
            x, hand = list(filter(
                lambda h: h[1].soft, enumerate(self.hands)
            ))[0]
            total_aces = len(
                list(
                    filter(lambda c: hasattr(c, 'face_card') and
                    c.face_card == "Ace", self.hands[x].cards)
                )
            )
            reduced_hand = self.hands[x].value - (10 * (total_aces - 1))
            self.hands[x].value = reduced_hand
            if self.hands[x].value > 21:
                return "BUST"
        if hand.value > 21:
            return "BUST"
        return "HIT"
