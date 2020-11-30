
import unittest
from unittest.mock import patch

from classes import Card, Dealer, Player, Hand


class TestCard(unittest.TestCase):
    '''Verify the value of a "J", "Q", or "K"
    card has a value of 10'''

    def setUp(self):
        self.joker_card = Card(10, "Spades", face_card="Joker")

    def test_card_face_card(self):
        self.assertEqual(self.joker_card.pip_value, 10)
        self.assertEqual(str(self.joker_card), "Joker of Spades")


class TestHard(unittest.TestCase):

    def setUp(self):
        card1, card2, card3, card4, card5 = [
            Card(10, "Spades"), Card(2, "Hearts"),
            Card(2, "Diamonds"), Card(10, "Hearts"), Card(8, "Clubs")
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


class TestDealerDealCards(unittest.TestCase):

    def setUp(self):
        self.dealer = Dealer()
        self.player = Player()
        self.cards = [
            Card(6, "Spade"), Card(10, "Spade"),
            Card(6, "Diamond"), Card(7, "Heart")
        ]

    def test_dealer_cards_same_pip(self):
        '''pc=player_cards; dc=dealer_cards'''

        pc, dc = self.dealer.deal(self.cards, self.player)
        self.assertListEqual(pc, [Card(6, "Spade"), Card(6, "Diamond")])
        self.assertListEqual(dc, [Card(10, "Spade"), Card(7, "Heart")])


class TestPlayerCheckCards(unittest.TestCase):
    '''Verify that a player'''

    def setUp(self):
        self.card_set = [Card(7, "Diamond"), Card(7, "Clubs")]
        self.player = Player()

    def test_player_cards_double_down(self):
        with patch("builtins.input", return_value="Y"):
            self.hand_status = self.player.check_cards(self.card_set)




if __name__ == "__main__":
    unittest.main()
