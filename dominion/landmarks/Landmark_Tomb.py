#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Landmark


###############################################################################
class Landmark_Tomb(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """When you trash a card, +1VP"""
        self.name = "Tomb"

    def hook_trash_card(self, game, player, card):
        player.output("Gained 1 VP from Tomb")
        player.add_score("Tomb", 1)


###############################################################################
class Test_Tomb(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, landmarks=["Tomb"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_trash(self):
        """Test Tomb"""
        cu = self.plr.piles[Piles.HAND]["Copper"]
        self.plr.trash_card(cu)
        self.assertEqual(self.plr.get_score_details()["Tomb"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
