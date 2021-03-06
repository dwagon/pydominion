#!/usr/bin/env python

import unittest
import Game
from Project import Project


###############################################################################
class Project_Innovation(Project):
    def __init__(self):
        Project.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "The first time you gain an Action card in each of your turns, you may set it aside. If you do, play it."
        self.name = "Innovation"
        self.cost = 6

    def hook_gain_card(self, game, player, card):
        if player.stats['gained']:
            return {}
        if not card.isAction():
            return {}
        ch = player.plrChooseOptions(
            "Play {} through Innovation?".format(card.name),
            ("Play card", True),
            ("Don't play", False)
        )
        if ch:
            player.addCard(card, 'hand')
            player.playCard(card, discard=False, costAction=False)
            # There are circumstances where playing the card can lead
            # to its removal from the player hand
            if card in player.hand:
                player.hand.remove(card)
            return {'destination': 'hand'}
        return {}


###############################################################################
class Test_Innovation(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Innovation'], initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        self.plr.assign_project('Innovation')
        self.plr.test_input = ['Play card']
        self.plr.start_turn()
        self.plr.gainCard('Moat')
        self.assertEqual(self.plr.hand.size(), 5 + 1 + 2)
        self.assertIsNotNone(self.plr.in_hand('Moat'))
        self.assertIsNone(self.plr.in_discard('Moat'))

    def test_dontplay(self):
        self.plr.assign_project('Innovation')
        self.plr.test_input = ["Don't play"]
        self.plr.start_turn()
        self.plr.gainCard('Moat')
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertIsNone(self.plr.in_hand('Moat'))
        self.assertIsNotNone(self.plr.in_discard('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
