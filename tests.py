
import unittest
from unittest.mock import patch

from classes import Card, Dealer, Player, Hand
from main import BlackjackTable
from exceptions import LowChipsException


class TestCard(unittest.TestCase):
    '''Verify the value of a "J", "Q", or "K"
    card has a value of 10'''

    def setUp(self):
        self.joker_card = Card(10, suit="Spades", face_card="Joker")

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

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.table = BlackjackTable()
        self.player = Player()

        self.player.chip_stack = 70

    def test_player_bet_no_wagered_bet(self):
        '''Verify that a player is continuosly prompted for a
        wager when no bet is placed before being dealt cards.'''

        with patch("builtins.input", side_effect=[0, 50]) as mock_input:
            with patch("builtins.print", return_value=None):
                self.player.bet()
        self.assertEqual(mock_input.call_count, 2)

    def test_player_bet_low_chip_stack(self):
        ''' Verify that chips are given back to a player
        when a bet is placed where the bet is greater
        than the total number of chips available.'''

        self.player.bets_made = 110
        with self.assertRaises(LowChipsException):
            self.player.bet()
        self.assertEqual(self.player.chip_stack, 70)

    def test_player_bet_high_chip_stack(self):
        ''' Verify that a player\'s chip stack is reduced
        when the bet placed is smaller than the total number
        of chips collected.'''
        self.player_bets_made = 0
        with patch("builtins.input", return_value=55) as mock_input:
            self.player.bet()
            mock_input.assert_called_once()
            self.assertEqual(self.player.chip_stack, 15)
            self.assertEqual(self.player.bets_made, 55)
#
    def test_player_bet_no_chips(self):
        '''Verify that a player cannot place a bet when
        their chip stack is 0.'''

        self.player.chip_stack = 0
        with self.assertRaises(LowChipsException):
            self.player.bet()

    def test_player_split_hand_unequal_pips(self):
        '''Verify that a player cannot split their hand
        when the cards are not of equal pip value.'''

        self.player.hands = [Hand(
            [Card(8, 'Clubs'), Card(9, 'Clubs')]
        )]
        with self.assertRaises(ValueError):
            self.player.split_hand()

    def test_player_split_hand_equal_pips(self):
        '''Verify that a player\'s hand is split into
        two hands when the two cards dealt to the player
        have the same pip value'''

        self.player.hands = [Hand(
            [Card(8, 'Clubs'), Card(8, 'Hearts')]
        )]
        hands, pos = self.player.split_hand()
        self.assertListEqual(hands,
            [Hand([Card(8, 'Clubs'), ]), Hand([Card(8, 'Hearts'), ])]
        )

    def test_player_check_hand_two_ace_cards(self):
        '''Verify that a player\'s hand is split into two hands
        when both cards dealt happen to be "Ace" face cards.'''
        self.player.chip_stack = 100
        self.player.bets_made = 25
        self.player.hands = [
            Hand([
                Card(11, 'Clubs', face_card='Ace'),
                Card(11, 'Hearts', face_card='Ace')
            ])
        ]
        with patch("builtins.print", return_value=None):
            hands, pos = self.player.check_hand(self.table.dealer)
            self.assertListEqual(hands, [
                Hand([Card(11, 'Clubs', face_card='Ace'), ]),
                Hand([Card(11, 'Hearts', face_card='Ace'), ])
            ]
            )
            self.assertEqual(len(self.player.hands), 2)
            self.assertEqual(self.player.bets_made, 50)


    def test_player_stand_one_ace_card(self):
        self.player.hands = [Hand(
            [Card(11, 'Clubs', face_card='Ace'), Card(11, 'Hearts', face_card='Ace')]
        )]
        with patch("builtins.input", return_value="11") as mock_input:
        hands, pos = self.player.stand()
        mock_input.assert_called_once()
        self.assertEqual(self.player.hands[0].value, 22)






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
