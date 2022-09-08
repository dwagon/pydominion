#!/usr/bin/env python
""" Test suite for Tokens """

import unittest
from dominion import Game


###############################################################################
class TestToken(unittest.TestCase):
    """Test suite for Tokens"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_place_token(self):
        """Ensure that when we place a token it is there"""
        self.assertEqual(self.plr.tokens["Trashing"], None)
        self.plr.place_token("Trashing", "Copper")
        self.assertNotEqual(self.plr.tokens["Trashing"], None)
        ans = self.plr.which_token("Copper")
        self.assertEqual(ans, ["Trashing"])

    def test_pickup(self):
        """Ensure we have smaller hand if -Card token in place"""
        self.plr.card_token = True
        self.plr.hand.empty()
        self.plr.pick_up_hand()
        self.assertEqual(self.plr.hand.size(), 4)
        self.assertFalse(self.plr.card_token)

    def test_short_draw(self):
        """Ensure we draw less if the -Card token is in place"""
        self.plr.card_token = True
        self.plr.hand.set()
        moat = self.g["Moat"].remove()
        self.plr.add_card(moat, "hand")
        self.assertEqual(self.plr.hand.size(), 1)
        self.plr.play_card(moat)
        # 2 for moat -1 for token
        self.assertEqual(self.plr.hand.size(), 2 - 1)
        self.assertFalse(self.plr.card_token)

    def test_action_token(self):
        """Does the +1 Action token work"""
        self.plr.place_token("+1 Action", "Moat")
        moat = self.g["Moat"].remove()
        self.plr.add_card(moat, "hand")
        self.assertEqual(self.plr.get_actions(), 1)
        self.plr.play_card(moat)
        self.assertEqual(self.plr.get_actions(), 1)

    def test_trashing_token(self):
        """Does the Trashing token work"""
        tsize = self.g.trashpile.size()
        self.plr.hand.set("Gold", "Province", "Duchy")
        self.plr.place_token("Trashing", "Moat")
        self.plr.test_input = ["trash province"]
        self.plr.set_coins(5)
        self.plr.buy_card(self.g["Moat"])
        self.assertEqual(self.g.trashpile.size(), tsize + 1)

    def test_cost_token(self):
        """Does the -Cost token work"""
        self.assertEqual(self.plr.get_coins(), 0)
        self.plr.place_token("-Cost", "Moat")
        self.plr.buy_card(self.g["Moat"])
        self.assertEqual(self.plr.get_coins(), 0)

    def test_card_token(self):
        """Does the +1 Card token work"""
        self.plr.hand.set()
        self.plr.place_token("+1 Card", "Moat")
        moat = self.g["Moat"].remove()
        self.plr.add_card(moat, "hand")
        self.assertEqual(self.plr.hand.size(), 1)
        self.plr.play_card(moat)
        # 2 for moat 1 for token
        self.assertEqual(self.plr.hand.size(), 2 + 1)

    def test_pluscoin_token(self):
        """Does the +1 Coin token work"""
        self.plr.place_token("+1 Coin", "Moat")
        moat = self.g["Moat"].remove()
        self.plr.add_card(moat, "hand")
        self.assertEqual(self.plr.get_coins(), 0)
        self.plr.play_card(moat)
        self.assertEqual(self.plr.get_coins(), 1)

    def test_buy_token(self):
        """Does the +1 Buy token work"""
        self.plr.place_token("+1 Buy", "Moat")
        moat = self.g["Moat"].remove()
        self.plr.add_card(moat, "hand")
        self.assertEqual(self.plr.get_buys(), 1)
        self.plr.play_card(moat)
        self.assertEqual(self.plr.get_buys(), 2)

    def test_journey_token(self):
        """Does the Journey token work"""
        self.assertTrue(self.plr.journey_token)
        self.plr.flip_journey_token()
        self.assertFalse(self.plr.journey_token)
        self.plr.flip_journey_token()
        self.assertTrue(self.plr.journey_token)

    def test_coin_token(self):
        """Does the -Coin token work"""
        # TODO

    def test_estate_token(self):
        """Does the Estate token work"""
        # TODO


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
