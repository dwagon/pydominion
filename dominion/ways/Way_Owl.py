#!/usr/bin/env python

import unittest
from dominion import Game
from dominion import Way


###############################################################################
class Way_Owl(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "Draw until you have 6 cards in hand."
        self.name = "Way of the Owl"

    def special(self, game, player):
        player.pick_up_hand(6)


###############################################################################
class Test_Owl(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            waycards=["Way of the Owl"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Moat"].remove()
        self.way = self.g.ways["Way of the Owl"]

    def test_play(self):
        """Perform a Owl"""
        self.plr.set_hand("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.hand.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
