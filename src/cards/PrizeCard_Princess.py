#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Princess(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'prize']
        self.base = 'cornucopia'
        self.name = "Princess"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 Buy; While this is in play, cards cost 2 less, but not less than 0."
        self.buys = 1

    def hook_cardCost(self, game, player, card):
        return -2


###############################################################################
class Test_Princess(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Tournament'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Princess'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.cardCost(self.g['Gold']), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
