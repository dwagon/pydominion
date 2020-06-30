#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_FlagBearer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'renaissance'
        self.desc = """When you gain or trash this, take the Flag."""
        self.name = 'Flag Bearer'
        # self.required_cards = [('Artifact', 'Flag')]
        self.needsartifacts = True
        self.cost = 4

    ###########################################################################
    def hook_gainThisCard(self, game, player):
        player.assign_artifact('Flag')

    ###########################################################################
    def hook_trashThisCard(self, game, player):
        player.assign_artifact('Flag')


###############################################################################
class Test_FlagBearer(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Flag Bearer'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.card = self.g['Flag Bearer'].remove()

    def test_gain(self):
        self.plr.gainCard('Flag Bearer')
        self.assertIsNotNone(self.plr.has_artifact('Flag'))

    def test_trash(self):
        card = self.g['Flag Bearer'].remove()
        self.plr.addCard(card, 'hand')
        self.plr.trashCard(card)
        self.assertIsNotNone(self.plr.has_artifact('Flag'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
