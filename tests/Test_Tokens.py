#!/usr/bin/env python
""" Test suite for Tokens """

import unittest

from dominion import Game, Piles


###############################################################################
class TestToken(unittest.TestCase):
    """Test suite for Tokens"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

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
        self.plr.piles[Piles.HAND].empty()
        self.plr.pick_up_hand()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)
        self.assertFalse(self.plr.card_token)

    def test_short_draw(self):
        """Ensure we draw less if the -Card token is in place"""
        self.plr.card_token = True
        self.plr.piles[Piles.HAND].set()
        moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(moat, Piles.HAND)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.plr.play_card(moat)
        # 2 for moat -1 for token
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2 - 1)
        self.assertFalse(self.plr.card_token)

    def test_action_token(self):
        """Does the +1 Action token work"""
        self.plr.place_token("+1 Action", "Moat")
        moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(moat, Piles.HAND)
        self.assertEqual(self.plr.actions.get(), 1)
        self.plr.play_card(moat)
        self.assertEqual(self.plr.actions.get(), 1)

    def test_trashing_token(self):
        """Does the Trashing token work"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Gold", "Province", "Duchy")
        self.plr.place_token("Trashing", "Moat")
        self.plr.test_input = ["trash province"]
        self.plr.coins.set(5)
        self.plr.buy_card("Moat")
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)

    def test_cost_token(self):
        """Does the -Cost token work"""
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.place_token("-Cost", "Moat")
        self.plr.buy_card("Moat")
        self.assertEqual(self.plr.coins.get(), 0)

    def test_card_token(self):
        """Does the +1 Card token work"""
        self.plr.piles[Piles.HAND].set()
        self.plr.place_token("+1 Card", "Moat")
        moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(moat, Piles.HAND)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.plr.play_card(moat)
        # 2 for moat 1 for token
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2 + 1)

    def test_pluscoin_token(self):
        """Does the +1 Coin token work"""
        self.plr.place_token("+1 Coin", "Moat")
        moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(moat, Piles.HAND)
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.play_card(moat)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_buy_token(self):
        """Does the +1 Buy token work"""
        self.plr.place_token("+1 Buy", "Moat")
        moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(moat, Piles.HAND)
        self.assertEqual(self.plr.buys.get(), 1)
        self.plr.play_card(moat)
        self.assertEqual(self.plr.buys.get(), 2)

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
