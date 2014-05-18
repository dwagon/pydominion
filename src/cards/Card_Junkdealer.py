#!/usr/bin/env python

import unittest
from Card import Card


class Card_Junkdealer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "+1 card, +1 action, +1 gold, trash a card"
        self.name = 'Junk Dealer'
        self.cards = 1
        self.actions = 1
        self.gold = 1
        self.cost = 2

    def special(self, game, player):
        tc = player.plrTrashCard()


###############################################################################
class Test_Junkdealer(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['junkdealer'])
        self.plr = self.g.players[0]
        self.jd = self.g['junkdealer'].remove()
        self.plr.addCard(self.jd, 'hand')

    def test_play(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.jd)
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(self.plr.t['gold'], 1)
        self.assertEqual(len(self.plr.hand), 6)
        self.assertEqual(self.g.trashpile, [])

    def test_trash(self):
        self.plr.test_input = ['1']
        self.plr.playCard(self.jd)
        self.assertEqual(len(self.plr.hand), 5)
        self.assertEqual(len(self.g.trashpile), 1)

###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF
