#!/usr/bin/env python

import unittest
import Game
from Project import Project


###############################################################################
class Project_StarChart(Project):
    def __init__(self):
        Project.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "When you shuffle, you may pick one of the cards to go on top."
        self.name = "Star Chart"
        self.cost = 3

    def hook_preShuffle(self, game, player):
        names = {_.name for _ in player.discardpile}
        choices = []
        for name in names:
            choices.append(("Put {} on top".format(name), name))
        opt = player.plrChooseOptions(
            "Pick a card to put on top of your deck",
            *choices
            )
        card = player.in_discard(opt)
        player.addCard(card, 'topdeck')
        player.discardpile.remove(card)


###############################################################################
class Test_StarChart(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Star Chart'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        self.plr.assign_project('Star Chart')
        self.plr.setDiscard('Copper', 'Copper', 'Silver', 'Gold', 'Estate', 'Gold')
        self.plr.setDeck()
        self.plr.test_input = ['Put Gold']
        c = self.plr.nextCard()
        self.assertEqual(c.name, 'Gold')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
