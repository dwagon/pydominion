#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import Game
from dominion import Way


###############################################################################
class Way_Squirrel(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+2 Cards at the end of this turn."
        self.name = "Way of the Squirrel"

    def special(self, game, player):
        player.newhandsize += 2


###############################################################################
class Test_Squirrel(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            waycards=["Way of the Squirrel"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Moat"].remove()
        self.way = self.g.ways["Way of the Squirrel"]

    def test_play(self):
        """Perform a Squirrel"""
        self.plr.add_card(self.card, "hand")
        self.plr.perform_way(self.way, self.card)
        self.plr.end_turn()
        self.assertEqual(self.plr.hand.size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
