#!/usr/bin/env python

import unittest
from dominion import Card, Game, Way, Piles


###############################################################################
class Way_Worm(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Exile an Estate from the Supply."
        self.name = "Way of the Worm"

    def special(self, game, player):
        player.exile_card("Estate")


###############################################################################
class Test_Worm(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            waycards=["Way of the Worm"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Worm"]

    def test_play(self):
        """Perform a Worm"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.perform_way(self.way, self.card)
        self.assertIn("Estate", self.plr.piles[Piles.EXILE])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
