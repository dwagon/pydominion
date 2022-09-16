#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import Game
from dominion import Way


###############################################################################
class Way_Camel(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Exile a Gold from the Supply."
        self.name = "Way of the Camel"

    def special(self, game, player):
        player.exile_card("Gold")


###############################################################################
class Test_Camel(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            waycards=["Way of the Camel"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Moat"].remove()
        self.way = self.g.ways["Way of the Camel"]

    def test_play(self):
        """Perform a Camel"""
        self.plr.add_card(self.card, "hand")
        self.plr.perform_way(self.way, self.card)
        self.assertIn("Gold", self.plr.exilepile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
