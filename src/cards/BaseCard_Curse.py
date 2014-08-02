#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Curse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'dominion'
        self.desc = "-1 VP"
        self.basecard = True
        self.playable = False
        self.purchasable = False
        self.name = 'Curse'
        self.cost = 0
        self.victory = -1


###############################################################################
class Test_Curse(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['witch'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['curse'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)

    def test_have(self):
        self.plr.addCard(self.card)
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Curse'], -1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
