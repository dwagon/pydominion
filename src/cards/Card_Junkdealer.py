#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Junkdealer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "+1 card, +1 action, +1 coin, trash a card"
        self.name = 'Junk Dealer'
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 2

    def special(self, game, player):
        player.plrTrashCard()


###############################################################################
class Test_Junkdealer(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Junk Dealer'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.jd = self.g['Junk Dealer'].remove()
        self.plr.setHand('Copper', 'Silver', 'Silver', 'Gold')
        self.plr.setDeck('Estate', 'Province', 'Duchy')
        self.plr.addCard(self.jd, 'hand')

    def test_play(self):
        tsize = self.g.trashSize()
        self.plr.test_input = ['finish']
        self.plr.playCard(self.jd)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.g.trashSize(), tsize)

    def test_trash(self):
        tsize = self.g.trashSize()
        self.plr.test_input = ['trash copper', 'finish']
        self.plr.playCard(self.jd)
        self.assertEqual(self.plr.handSize(), 4)
        self.assertEqual(self.g.trashSize(), tsize + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
