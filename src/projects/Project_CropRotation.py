#!/usr/bin/env python

import unittest
import Game
from Project import Project


###############################################################################
class Project_CropRotation(Project):
    def __init__(self):
        Project.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = (
            "At the start of your turn, you may discard a Victory card for +2 Cards."
        )
        self.name = "Crop Rotation"
        self.cost = 6

    def hook_start_turn(self, game, player):
        vics = [_ for _ in player.hand if _.isVictory()]
        if not vics:
            return
        card = player.plrDiscardCards(
            prompt="Crop Rotation: Discard a victory for +2 Cards", cardsrc=vics
        )
        if card:
            player.pickupCards(2)


###############################################################################
class Test_CropRotation(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=["Crop Rotation"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_cost(self):
        self.plr.assign_project("Crop Rotation")
        self.plr.setHand("Copper", "Silver", "Estate")
        self.plr.test_input = ["Discard Estate"]
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 3 + 2 - 1)
        self.assertIsNotNone(self.plr.in_discard("Estate"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
