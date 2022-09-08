#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Necropolis """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Necropolis(Card.Card):
    """Necropolis"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_SHELTER]
        self.base = Game.DARKAGES
        self.desc = "0VP; +2 Actions"
        self.name = "Necropolis"
        self.cost = 1
        self.actions = 2
        self.victory = 0
        self.purchasable = False


###############################################################################
class Test_Necropolis(unittest.TestCase):
    """Test Necropolis"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Shelters"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        """Test Play"""
        self.plr.hand.set("Necropolis", "Estate")
        card = self.plr.hand["Necropolis"]
        self.assertEqual(self.plr.get_actions(), 1)
        self.plr.play_card(card)
        self.assertEqual(self.plr.get_actions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
