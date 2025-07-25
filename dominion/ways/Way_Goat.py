#!/usr/bin/env python

import unittest

from dominion import Card, Game, Way, Piles


###############################################################################
class Way_Goat(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Trash a card from your hand."
        self.name = "Way of the Goat"

    def special(self, game, player):
        player.plr_trash_card()


###############################################################################
class Test_Goat(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, ways=["Way of the Goat"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Goat"]

    def test_play(self):
        """Perform a Goat"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Copper"]
        self.plr.perform_way(self.way, self.card)
        self.assertIn("Copper", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
