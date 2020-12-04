
import unittest
from unittest.mock import patch

from classes import Card, Dealer, Player, Hand
from exceptions import LowChipsException

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player()

        self.player.chip_stack = 70

    # def test_player_bet_no_wagered_bet(self):
    #     with patch("builtins.input", return_value=0) as mock_input:
    #         with self.assertRaises(ValueError):
    #             self.player.bet()
    #             mock_input.assert_called_once()

    def test_player_bet_low_chip_stack(self):
        self.player.bets_made = 110
        with self.assertRaises(LowChipsException):
            self.player.bet()
        self.assertEqual(self.player.chip_stack, 70)

    def test_player_bet_high_chip_stack(self):
        self.player_bets_made = 0
        with patch("builtins.input", return_value=55) as mock_input:
            self.player.bet()
            mock_input.assert_called_once()
            self.assertEqual(self.player.chip_stack, 15)
            self.assertEqual(self.player.bets_made, 55)

    def test_player_bet_no_chips(self):
        self.player.chip_stack = 0
        with self.assertRaises(LowChipsException):
            self.player.bet()

    def test_player_split_hand_unequal_pips(self):
        self.player.hands = [Hand(
            [Card(8, 'Clubs'), Card(9, 'Clubs')]
        )]
        with self.assertRaises(ValueError):
            self.player.split_hand()

    def test_player_split_hand_equal_pips(self):
        self.player.hands = [Hand(
            [Card(8, 'Clubs'), Card(8, 'Hearts')]
        )]
        hands, pos = self.player.split_hand()
        self.assertListEqual(hands,
            [Hand([Card(8, 'Clubs'), ]), Hand([Card(8, 'Hearts'), ])]
        )

    # def test_player_hit_or_stand(self):
    #     with patch("builtins.input", return_value="STAND") as mock_input:
    #         blackjack_play = self.player.hit_or_stand()
    #         mock_input.assert_called_once()
    #         self.assertTupleEqual(blackjack_play, (self.player.hands, "STAND"))
#
#
class TestCard(unittest.TestCase):
    '''Verify the value of a "J", "Q", or "K"
    card has a value of 10'''

    def setUp(self):
        self.joker_card = Card(pip=10, suit="Spades", face_card="Joker")

    def test_card_face_card(self):
        self.assertEqual(self.joker_card.pip, 10)
        self.assertEqual(str(self.joker_card), "Joker of Spades")


class TestHard(unittest.TestCase):

    def setUp(self):
        card1, card2, card3, card4, card5 = [
            Card(pip=10, suit="Spades"),
            Card(pip=2, suit="Hearts"),
            Card(pip=2, suit="Diamonds"),
            Card(pip=10, suit="Hearts"),
            Card(pip=8, suit="Clubs")
        ]
        self.hand1 = Hand([card1, card3])
        self.hand2 = Hand([card2, card4])
        self.hand3 = Hand([card3, card5])
        self.hand4 = Hand([card2, card3])
        self.hand5 = Hand([card1, card5])

    def test_eq_hands(self):
        self.assertTrue(self.hand1 == self.hand2)

    def test_cards_gte_or_lte(self):
        self.assertTrue(self.hand2 >= self.hand3)
        self.assertTrue(self.hand4 <= self.hand5)

    def test_hand_value(self):
        self.assertEqual(self.hand1.value, 12)

# #
# # class TestPlayerCheckCards(unittest.TestCase):
# #     '''Verify that a player'''
# #
# #     def setUp(self):
# #         self.card_set = [Card(7, "Diamond"), Card(7, "Clubs")]
# #         self.player = Player()
# #
# #     def test_player_cards_double_down(self):
# #         with patch("builtins.input", return_value="Y"):
# #             self.hand_status = self.player.check_cards(self.card_set)
#



if __name__ == "__main__":
    unittest.main()
