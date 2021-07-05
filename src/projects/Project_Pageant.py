#!/usr/bin/env python

import unittest
import Game
from Project import Project


###############################################################################
class Project_Pageant(Project):
    def __init__(self):
        Project.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "At the end of your Buy phase, you may pay 1 Coin for +1 Coffers."
        self.name = "Pageant"
        self.cost = 3

    def hook_endBuyPhase(self, game, player):
        options = []
        if player.coin == 0:
            return
        for num in range(player.coin + 1):
            options.append(("Buy {} Coffers for {} Coin".format(num, num), num))
        pick = player.plrChooseOptions("Exchange coin for coffers", *options)
        player.gainCoffer(pick)
        player.coin -= pick


###############################################################################
class Test_Pageant(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=["Pageant"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        numc = self.plr.getCoffer()
        self.plr.assign_project("Pageant")
        self.plr.setCoin(5)
        self.plr.test_input = ["End Phase", "4"]
        self.plr.buy_phase()
        self.assertEqual(self.plr.getCoffer(), numc + 4)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
