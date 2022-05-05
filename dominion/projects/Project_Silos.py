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
            ans = player.plr_choose_options("Discard how many coppers? ", *choices)
            for _ in range(ans):
                cu = player.hand["Copper"]
                player.discard_card(cu)
                player.pickup_cards(1)


###############################################################################
class Test_Silos(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initprojects=["Silos"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        self.plr.assign_project("Silos")
        self.plr.deck.set("Estate", "Estate", "Estate")
        self.plr.hand.set("Copper", "Estate", "Copper", "Province")
        self.plr.test_input = ["2"]
        self.plr.start_turn()
        self.assertIsNotNone(self.plr.discardpile["Copper"])
        self.assertNotIn("Copper", self.plr.hand)
        self.assertEqual(self.plr.hand.size(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
