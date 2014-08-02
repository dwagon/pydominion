#!/usr/bin/env python

import unittest
from Card import Card


class Card_Storeroom(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "Discard any number of cards twice"
        self.name = 'Store Room'
        self.buys = 1
        self.cost = 3

    def special(self, game, player):
        """ Discard any number of cards. +1 Card per card discarded.
            Discard any number of cards. +1 GP per card discarded the
            second time"""
        player.output("Discard any number of cards. +1 Card per card discarded")
        todiscard = player.plrDiscardCards(0, anynum=True)
        player.pickupCards(len(todiscard))
        player.output("Discard any number of cards. +1 GP per card discarded")
        todiscard = player.plrDiscardCards(0, anynum=True)
        player.addCoin(len(todiscard))


###############################################################################
class Test_Storeroom(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['storeroom'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['storeroom'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a store room """
        self.plr.test_input = ['0', '0']
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.getBuys(), 2)
        self.assertTrue(self.plr.discardpile.isEmpty())

    def test_discardonce(self):
        """ Storeroom: Only discard during the first discard phase """
        self.plr.test_input = ['1', '0', '0']
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.handSize(), 5 - 1 + 1)
        self.assertEquals(self.plr.discardSize(), 1)
        self.assertEquals(self.plr.getBuys(), 2)

    def test_discardtwice(self):
        """ Storeroom: Discard during the both discard phases """
        self.plr.test_input = ['1', '0', '1', '0']
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.handSize(), 5 - 1)
        self.assertEquals(self.plr.discardSize(), 2)
        self.assertEquals(self.plr.getBuys(), 2)
        self.assertEquals(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
