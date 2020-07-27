#!/usr/bin/env python

import unittest
import Game
from Project import Project


###############################################################################
class Project_Silos(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "At the start of your turn, discard any number of Coppers, revealed, and draw that many cards."
        self.name = "Silos"
        self.cost = 4

    def hook_start_turn(self, game, player):
        cus = [_ for _ in player.hand if _.name == 'Copper']
        if cus:
            choices = []
            for num in range(len(cus)+1):
                choices.append(("Silo: Discard {} Coppers".format(num), num))
            ans = player.plrChooseOptions("Discard how many coppers? ", *choices)
            for _ in range(ans):
                cu = player.inHand('Copper')
                player.discardCard(cu)
                player.pickupCards(1)


###############################################################################
class Test_Silos(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Silos'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        self.plr.assign_project('Silos')
        self.plr.setDeck('Estate', 'Estate', 'Estate')
        self.plr.setHand('Copper', 'Estate', 'Copper', 'Province')
        self.plr.test_input = ['2']
        self.plr.start_turn()
        self.assertIsNotNone(self.plr.inDiscard('Copper'))
        self.assertIsNone(self.plr.inHand('Copper'))
        self.assertEqual(self.plr.handSize(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
