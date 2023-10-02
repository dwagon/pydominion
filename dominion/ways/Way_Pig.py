#!/usr/bin/env python

import unittest
from dominion import Card, Game, Way, Piles


###############################################################################
class Way_Pig(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+1 Card; +1 Action"
        self.name = "Way of the Pig"
        self.cards = 1
        self.actions = 1


###############################################################################
class Test_Pig(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            ways=["Way of the Pig"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Pig"]

    def test_play(self):
        """Perform a Pig"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
