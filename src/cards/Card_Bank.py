#!/usr/bin/env python

import unittest
from Card import Card


class Card_Bank(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'prosperity'
        self.desc = "+1Gold per treasure in play"
        self.name = 'Bank'
        self.cost = 7

    def hook_coinvalue(self, game, player):
        """ When you play this it is worth 1 per treasure card you
            have in play (counting this) """
        num_treas = sum([1 for c in player.played if c.isTreasure()])
        return num_treas


###############################################################################
class Test_Bank(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bank'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Bank'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_gainnothing(self):
        self.plr.setPlayed('Estate', 'Estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_gainsomething(self):
        self.plr.setPlayed('Copper', 'Silver', 'Estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
