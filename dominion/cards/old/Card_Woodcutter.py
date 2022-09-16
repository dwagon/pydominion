#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Woodcutter"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_Woodcutter(Card.Card):
    """Woodcutter"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "+1 buys, +2 coin"
        self.name = "Woodcutter"
        self.buys = 1
        self.coin = 2
        self.cost = 3


###############################################################################
class Test_Woodcutter(unittest.TestCase):
    """Test Woodcutter"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Woodcutter"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Woodcutter"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the woodcutter"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.buys.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
