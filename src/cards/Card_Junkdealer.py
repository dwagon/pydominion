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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['junkdealer'])
        self.plr = self.g.playerList(0)
        self.jd = self.g['junkdealer'].remove()
        self.plr.setHand('copper', 'silver', 'silver', 'gold')
        self.plr.setDeck('estate', 'province', 'duchy')
        self.plr.addCard(self.jd, 'hand')

    def test_play(self):
        self.plr.test_input = ['finish']
        self.plr.playCard(self.jd)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.g.trashpile, [])

    def test_trash(self):
        self.plr.test_input = ['trash copper', 'finish']
        self.plr.playCard(self.jd)
        self.assertEqual(self.plr.handSize(), 4)
        self.assertEqual(self.g.trashSize(), 1)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
