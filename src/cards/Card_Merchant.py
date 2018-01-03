#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Merchant(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+1 Card; +1 Action; The first time you play a Silver this turn, +1 Coin."
        self.name = 'Merchant'
        self.actions = 1
        self.cards = 1
        self.cost = 3

    def hook_spendValue(self, game, player, card):
        if card.name != 'Silver':
            return 0
        ag_count = player.played.count('Silver')
        if ag_count == 1:
            return 1
        else:
            return 0


###############################################################################
class Test_Merchant(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Merchant'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Merchant'].remove()
        self.s1 = self.g['Silver'].remove()
        self.s2 = self.g['Silver'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 6)
        self.plr.addCard(self.s1, 'hand')
        self.plr.playCard(self.s1)
        self.assertEqual(self.plr.getCoin(), 3)
        self.plr.addCard(self.s2, 'hand')
        self.plr.playCard(self.s2)
        self.assertEqual(self.plr.getCoin(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
