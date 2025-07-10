#!/usr/bin/env python

import unittest

from dominion import Card, Game, Way, Piles


###############################################################################
class Way_Otter(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+2 Cards"
        self.name = "Way of the Otter"
        self.cards = 2


###############################################################################
class TestOtter(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            ways=["Way of the Otter"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Otter"]

    def test_play(self):
        """Perform a Otter"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
