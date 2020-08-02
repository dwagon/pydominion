#!/usr/bin/env python

import unittest
import Game
from Project import Project


###############################################################################
class Project_Citadel(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "The first time you play an Action card during each of your turns, play it again afterward."
        self.name = "Citadel"
        self.cost = 8

    def hook_postAction(self, game, player, card):
        if player.playedSize() == 1:
            player.output("Citadel plays {} again".format(card.name))
            player.playCard(card, discard=False, costAction=False, postActionHook=False)


###############################################################################
class Test_Citadel(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Citadel'], initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.assign_project('Citadel')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 + 2 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
