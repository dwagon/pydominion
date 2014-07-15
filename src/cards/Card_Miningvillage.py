#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Miningvillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+1 card, +2 actions, trash self for +2 coin"
        self.name = 'Mining Village'
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def special(self, game, player):
        """ You may trash this card immediately. If you do +2 coin """
        trash = player.plrChooseOptions(
            "Choose one",
            ('Do nothing', False), ('Trash mining village for +2 coin', True))
        if trash:
            player.output("Trashing mining village")
            player.addCoin(2)
            player.trashCard(self)


###############################################################################
class Test_Miningvillage(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['miningvillage'])
        self.plr = list(self.g.players.values())[0]
        self.card = self.g['miningvillage'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a Mining Village """
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.g.trashpile, [])
        self.assertEqual(self.plr.played[-1].name, 'Mining Village')

    def test_trash(self):
        """ Trash the mining village """
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.played, [])
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.g.trashpile[-1].name, 'Mining Village')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
