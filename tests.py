
import unittest
from unittest.mock import patch

from classes import Card, Hand, Player, Dealer
from exceptions import BettingError, HandSplitError

import utils

class TestCard(unittest.TestCase):

    def setUp(self):
        self.pip_card = Card(9, "Clubs")
        self.face_card = Card(10, "Clubs", face_card="King")

    def test_pip_card(self):
        self.assertEqual(str(self.pip_card), "9 of Clubs")
        self.assertEqual(self.pip_card.pip, 9)

    def test_face_card(self):
        self.assertEqual(str(self.face_card), "King of Clubs")
        self.assertEqual(self.face_card.pip, 10)


class TestHand(unittest.TestCase):

    def setUp(self):
        card1, card2, card3, card4, card5, card6 = [
            Card(10, "Spades"),
            Card(2, "Hearts"),
            Card(2, "Diamonds"),
            Card(10, "Hearts"),
            Card(11, "Clubs", face_card="Ace"),
            Card(8, "Clubs")
        ]
        self.hand1 = Hand([card1, card3])
        self.hand2 = Hand([card2, card4])
        self.hand3 = Hand([card3, card5])
        self.hand4 = Hand([card2, card3])
        self.hand5 = Hand([card1, card5])
        self.hand6 = Hand([card1, card6])

    def test_hand__str__(self):
        self.assertEqual(str(self.hand1), "10 of Spades,2 of Diamonds")

    def test_card__repr__(self):
        self.assertEqual(repr(self.hand6), f"Hand([Card(10, Spades), Card(8, Clubs)])")

    def test_hand_number_of_cards(self):
        self.assertEqual(len(self.hand1), 2)

    def test_hand_dealt_hard_hand(self):
        self.assertEqual(self.hand6.value, 18)
        self.assertFalse(self.hand6.soft)

    def test_hand_dealt_soft_hand(self):
        self.assertEqual(self.hand5.value, 21)
        self.assertTrue(self.hand5.soft)

    def test_hands_equal(self):
        self.assertTrue(self.hand1 == self.hand2)

    def test_hand_less_than(self):
        self.assertTrue(self.hand3 < self.hand5)

    def test_hand_greater_than(self):
        self.assertTrue(self.hand2 > self.hand4)


class TestHandDescriptor(unittest.TestCase):

    def setUp(self):
        card1 = Card(8, 'Spades')
        card2 = Card(9, 'Spades')
        self.hand = Hand([card1, card2])

    def test_hand__get__value(self):
        self.assertEqual(self.hand.value, 17)

    def test_hand__set__value(self):
        value = self.hand.value + 3
        self.assertEqual(value, 20)

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player()
        self.dealer = Dealer()
        self.player.chips = 100
        self.player._bet = 0

    def test_player_bet_no_bet(self):
        '''Verify that a player is informed that no cards
        can be dealt until a bet is placed'''

        with patch("builtins.print", return_value=None):
            with patch("builtins.input", side_effect=['0', '50']) as mock_bet:
                self.player.bet()
            self.assertEqual(mock_bet.call_count, 2)
            self.assertEqual(self.player.chips, 50)

    def test_player_bet_no_chips(self):
        '''Verify that a player cannot place a bet
        when there are no more chips to bet with.'''

        self.player.chips = 0
        with patch("builtins.print", return_value=None):
            with self.assertRaises(BettingError):
                self.player.bet()
                self.assertEqual(self.player.chips, 0)

    def test_player_bet_with_chips_and_bet(self):
        '''Verify that a bet is placed when a player
        has chips aviailable to bet with.'''

        self.player._bet = 35
        with patch("builtins.print", return_value=0):
            self.player.bet()
            self.assertEqual(self.player.chips, 65)
            self.assertEqual(self.player._bet, 70)

    def test_player_split_hand_unequal_pips(self):
        '''Verify that a player cannot split their hand when
        the pip values of each card is not equal.'''

        hand = Hand([
            Card(8, "Spades"),
            Card(9, "Diamonds")
        ])

        with self.assertRaises(HandSplitError):
            self.player.split_hand(hand)

    def test_player_split_hand_equal_pips(self):
        '''Verify that a player can split their hand when
        the pip values of each card is equal.'''

        hand = Hand([
            Card(8, "Spades"),
            Card(8, "Hearts")
        ])

        hands = self.player.split_hand(hand)
        self.assertEqual(len(hands), 2)

    def test_player_check_hand(self):
        '''Verify that if a player initially receives two
        cards that both happen to have the same pip value
        that the hand is split into two hands.'''

        self.player.hands = [Hand([Card(8, "Clubs"), Card(8, "Hearts")])]
        self.dealer.hands = [Hand([Card(10, "Diamonds"), Card(3, "Clubs")])]
        self.player.chips = 100
        self.player._bet = 40

        with patch("builtins.print", return_value=None):
            with patch("builtins.input", return_value="SPLIT") as mock_bet:

                pos = self.player.check_hand(self.dealer.hands[0], self.player.hands[0])
                self.assertEqual(self.player.chips, 60)
                self.assertEqual(self.player._bet, 80)
                self.assertEqual(pos, "SPLIT")

    def test_player_check_hand_low_chips(self):
        '''Verify a player is handed back chips upon
        trying to split or double down a hand when
        they have a low chip stack.'''

        self.player.hands = [Hand([Card(8, "Clubs"), Card(8, "Hearts")])]
        self.dealer.hands = [Hand([Card(10, "Diamonds"), Card(10, "Hearts", face_card="King")])]
        self.player.chips = 30
        self.player._bet = 40

        with patch("builtins.print", return_value=None):
            with patch("builtins.input", side_effect=["SPLIT", 'DOUBLE DOWN', "HIT"]) as mock_bet:
                self.player.check_hand(self.dealer.hands[0], self.player.hands[0])
                self.assertEqual(mock_bet.call_count, 3)
                self.assertEqual(self.player.chips, 30)
                self.assertEqual(self.player._bet, 40)

    def test_player_check_hand_good_bet_invalid_double_down(self):
        '''Verify that chips are handed back to a player if a
        valid bet is placed but cannot double down due to having
        too many cards'''

        self.player.hands = [Hand([Card(8, "Clubs"), Card(8, "Hearts"), Card(3, "Diamonds")])]
        self.dealer.hands = [Hand([Card(10, "Diamonds"), Card(10, "Hearts", face_card="King")])]
        self.player.chips = 85
        self.player._bet = 25

        with patch("builtins.print", return_value=None):
            with patch("builtins.input", side_effect=["DOUBLE DOWN", "STAND"]) as mock_play:
                self.player.check_hand(self.dealer.hands[0], self.player.hands[0])
                self.assertEqual(mock_play.call_count, 2)
                self.assertEqual(self.player.chips, 85)
                self.assertEqual(self.player._bet, 25)

    def test_player_hit_no_active_soft_convert(self):
        '''Verify that a player\'s hand is a soft hand when
        Aces are dealt.'''

        self.player.hands = [Hand([
                Card(11, 'Spades', face_card="Ace"),
                Card(7, 'Spades'),
                Card(11, "Diamonds", face_card="Ace")
            ])]
        pos = self.player.hit(self.player.hands[0])
        self.assertEqual(pos, "HIT")
        self.assertEqual(self.player.hands[0].value, 19)

    def test_player_hit_active_soft_convert(self):
        '''Verify that a player\'s hand results in a BUST
        when the hand is calculated as a soft hand'''

        self.player.hands = [Hand([
                Card(11, 'Spades', face_card="Ace"),
                Card(11, "Diamonds", face_card="Ace"),
                Card(11, "Hearts", face_card="Ace"),
                Card(11, "Clubs", face_card="Ace"),
                Card(10, "Hearts", face_card="Queen"),
                Card(9, "Clubs")
            ])]

        pos = self.player.hit(self.player.hands[0])
        self.assertTrue(pos == "BUST")
        self.assertEqual(self.player.hands[0].value, 23)

    def test_player_hit_hard_hand(self):
        '''Verify that a player\'s hard hand busts when
        its value exceeds 21.'''
        self.player.hands = [Hand([
                Card(9, "Spades"),
                Card(8, "Diamonds"),
                Card(6, "Hearts")
            ])]

        pos = self.player.hit(self.player.hands[0])
        self.assertTrue(pos == "BUST")
        self.assertEqual(self.player.hands[0].value, 23)

    def test_player_double_down_too_many_cards(self):

        cards = [
            Card(8, "Clubs"), Card(3, "Clubs", "Queen"), Card(2, "Clubs")
        ]
        hand = Hand(cards)
        with self.assertRaises(ValueError):
            self.player.double_down(hand)





class TestDealer(unittest.TestCase):

    def setUp(self):
        self.dealer = Dealer()
        self.player = Player()
        self.dealer.hands = [Hand([Card(9, "Clubs"), Card(2, "Clubs")])]

    def test_dealer_deal_hands(self):
        cards = [Card(4, "Hearts"), Card(9, "Hearts"), Card(2, "Hearts"), Card(8, "Clubs")]

        hands_dealt = self.dealer.deal_hands(cards, self.player)
        self.assertTrue(all(len(hand) == 2 for hand in hands_dealt))

    def test_dealer_hit_stand(self):
        with patch.object(Dealer, "deal_card", return_value=Card(7, 'Clubs')):
            pos = self.dealer.hit([])
            self.assertEqual(len(self.dealer.hands[0]), 3)
            self.assertEqual(self.dealer.hands[0].value, 18)



if __name__ == "__main__":
    unittest.main()
