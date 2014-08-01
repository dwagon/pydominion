#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Oasis(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'hinterlands'
        self.desc = "+1 card, +1 action, +1 coin, discard 1 card"
        self.name = 'Oasis'
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 3

    def special(self, game, player):
        """ Discard a card"""
        player.plrDiscardCards()


###############################################################################
class Test_Oasis(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['oasis'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['oasis'].remove()
        self.plr.setHand('gold', 'copper', 'copper', 'copper', 'copper')
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play an oasis """
        self.plr.test_input = ['select gold', 'finish']
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.getActions(), 1)
        self.assertEquals(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
