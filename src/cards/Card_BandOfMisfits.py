#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_BandOfMisfits(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = """Play this as if it were an Action card in the Supply costing less than it that you choose. This is that card until it leaves play."""
        self.name = 'Band of Misfits'
        self.cost = 5

    def special(self, game, player):
        pass    # TODO


###############################################################################
class Test_BandOfMisfits(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Band of Misfits'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Band of Misfits'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
