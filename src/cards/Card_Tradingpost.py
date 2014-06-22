#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Tradingpost(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "Trash 2 cards for a silver"
        self.name = "Trading Post"
        self.cost = 5

    def special(self, game, player):
        """ Trash 2 card from your hand. If you do, gain a Silver card; put it into your hand"""
        player.output("Trash two cards to gain a silver")
        num = min(2, len(player.hand))
        trash = player.plrTrashCard(num=num)
        if len(trash) == 2:
            player.gainCard('silver', 'hand')
            player.addGold(2)
        else:
            player.output("Not enough cards trashed")


###############################################################################
class Test_Tradingpost(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['tradingpost'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['tradingpost'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play Trading Post """
        self.plr.test_input = ['1', '2', '0']
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.inHand('Silver'))
        self.assertEqual(len(self.g.trashpile), 2)

    def test_trash_little(self):
        """ Play a trading post but don't trash enough """
        self.plr.test_input = ['1', '0']
        self.plr.playCard(self.card)
        self.assertFalse(self.plr.inHand('Silver'))
        self.assertEqual(len(self.g.trashpile), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
#EOF
