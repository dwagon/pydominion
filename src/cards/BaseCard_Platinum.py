#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Platinum(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'prosperity'
        self.desc = "+5 coin"
        self.name = 'Platinum'
        self.playable = False
        self.basecard = True
        self.coin = 5
        self.cost = 9


###############################################################################
class Test_Platinum(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, prosperity=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Platinum'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a platinum """
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.getCoin(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
