
import unittest
from unittest.mock import patch

from classes import Card, Dealer, Player, Hand

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player()
        self.player.hands = [Hand(
            [Card(8, 'Clubs'), Card(8, 'Hearts')]
        )]

    def test_player_bet_no_chips(self):
        with patch("builtins.input", return_value=0) as mock_input:
            with self.assertRaises(ValueError):
                self.player.bet()
                mock_input.assert_called_once()


    def test_player_check_cards_split(self):
        with patch("builtins.input", return_value="Y") as mock_input:
            blackjack_play = self.player.check_hand()
            mock_input.assert_called_once()
            self.assertTupleEqual(blackjack_play, (
                [[Card(8, 'Clubs'), ], [Card(8, 'Hearts'), ]], "split")
            )

    def test_player_hit_or_stand(self):
        with patch("builtins.input", return_value="STAND") as mock_input:
            blackjack_play = self.player.hit_or_stand()
            mock_input.assert_called_once()
            self.assertTupleEqual(blackjack_play, (self.player.hands[0], "STAND"))
#
#
# class TestCard(unittest.TestCase):
#     '''Verify the value of a "J", "Q", or "K"
#     card has a value of 10'''
#
#     def setUp(self):
#         self.joker_card = Card(pip=10, suit="Spades", face_card="Joker")
#
#     def test_card_face_card(self):
#         self.assertEqual(self.joker_card.pip, 10)
#         self.assertEqual(str(self.joker_card), "Joker of Spades")
#
#
# class TestHard(unittest.TestCase):
#
#     def setUp(self):
#         card1, card2, card3, card4, card5 = [
#             Card(pip=10, suit="Spades"),
#             Card(pip=2, suit="Hearts"),
#             Card(pip=2, suit="Diamonds"),
#             Card(pip=10, suit="Hearts"),
#             Card(pip=8, suit="Clubs")
#         ]
#         self.hand1 = Hand([card1, card3])
#         self.hand2 = Hand([card2, card4])
#         self.hand3 = Hand([card3, card5])
#         self.hand4 = Hand([card2, card3])
#         self.hand5 = Hand([card1, card5])
#
#     def test_eq_hands(self):
#         self.assertTrue(self.hand1 == self.hand2)
#
#     def test_cards_gte_or_lte(self):
#         self.assertTrue(self.hand2 >= self.hand3)
#         self.assertTrue(self.hand4 <= self.hand5)
#
#     def test_hand_value(self):
#         self.assertEqual(self.hand1.value, 12)
#
#
# # class TestDealerDealCards(unittest.TestCase):
# #
# #     def setUp(self):
# #         self.dealer = Dealer()
# #         self.player = Player()
# #         self.cards = [
# #             Card(pip=6, suit="Spade"), Card(pip=10, suit="Spade"),
# #             Card(pip=6, suit="Diamond"), Card(pip=7, suit="Heart")
# #         ]
# #
# #     def test_dealer_cards_same_pip(self):
# #         '''pc=player_cards; dc=dealer_cards'''
# #
# #         pc, dc = self.dealer.deal(self.cards, self.player)
# #         self.assertListEqual(pc, [Card(pip=6, suit="Spade"), Card(pip=6, suit="Diamond")])
# #         self.assertListEqual(dc, [Card(pip=10, suit="Spade"), Card(pip=7, suit="Heart")])
# # #
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
