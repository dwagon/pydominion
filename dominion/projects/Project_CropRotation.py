#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Project


###############################################################################
class Project_CropRotation(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = (
            "At the start of your turn, you may discard a Victory card for +2 Cards."
        )
        self.name = "Crop Rotation"
        self.cost = 6

    def hook_start_turn(self, game, player):
        vics = [_ for _ in player.piles[Piles.HAND] if _.isVictory()]
        if not vics:
            return
        card = player.plr_discard_cards(
            prompt="Crop Rotation: Discard a victory for +2 Cards", cardsrc=vics
        )
        if card:
            player.pickup_cards(2)


###############################################################################
class Test_CropRotation(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, projects=["Crop Rotation"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_cost(self):
        self.plr.assign_project("Crop Rotation")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate")
        self.plr.test_input = ["Discard Estate"]
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3 + 2 - 1)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Estate"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
