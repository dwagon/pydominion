#!/usr/bin/env python

import unittest
from dominion import Game, Project


###############################################################################
class Project_Silos(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "At the start of your turn, discard any number of Coppers, revealed, and draw that many cards."
        self.name = "Silos"
        self.cost = 4

    def hook_start_turn(self, game, player):
        cus = [_ for _ in player.hand if _.name == "Copper"]
        if cus:
            choices = []
            for num in range(len(cus) + 1):
                choices.append(("Silo: Discard {} Coppers".format(num), num))
            ans = player.plrChooseOptions("Discard how many coppers? ", *choices)
            for _ in range(ans):
                cu = player.in_hand("Copper")
                player.discardCard(cu)
                player.pickupCards(1)


###############################################################################
class Test_Silos(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=["Silos"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        self.plr.assign_project("Silos")
        self.plr.set_deck("Estate", "Estate", "Estate")
        self.plr.set_hand("Copper", "Estate", "Copper", "Province")
        self.plr.test_input = ["2"]
        self.plr.start_turn()
        self.assertIsNotNone(self.plr.in_discard("Copper"))
        self.assertIsNone(self.plr.in_hand("Copper"))
        self.assertEqual(self.plr.hand.size(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
