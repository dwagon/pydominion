#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Stockpile """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Stockpile(Card.Card):
    """Stockpile"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = """3 Coin; +1 Buy; When you play this, Exile it."""
        self.name = "Stockpile"
        self.coin = 3
        self.buys = 1
        self.cost = 3

    def special(self, game, player):
        player.exile_card(self)


###############################################################################
class Test_Stockpile(unittest.TestCase):
    """Test Stockpile"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Stockpile"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Stockpile"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the card"""
        self.plr.play_card(self.card)
        self.assertIn("Stockpile", self.plr.exilepile)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.coins.get(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
