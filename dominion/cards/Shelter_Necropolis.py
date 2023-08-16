#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Necropolis """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Necropolis(Card.Card):
    """Necropolis"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.SHELTER]
        self.base = Card.CardExpansion.DARKAGES
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
        self.plr.piles[Piles.HAND].set("Necropolis", "Estate")
        card = self.plr.piles[Piles.HAND]["Necropolis"]
        self.assertEqual(self.plr.actions.get(), 1)
        self.plr.play_card(card)
        self.assertEqual(self.plr.actions.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
