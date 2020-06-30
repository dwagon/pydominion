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
        num = min(2, player.handSize())
        trash = player.plrTrashCard(num=num, prompt="Trash two cards to gain a silver")
        if len(trash) == 2:
            player.gainCard('Silver', 'hand')
            player.addCoin(2)
        else:
            player.output("Not enough cards trashed")


###############################################################################
class Test_Tradingpost(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Trading Post'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.card = self.g['Trading Post'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play Trading Post """
        tsize = self.g.trashSize()
        self.plr.test_input = ['1', '2', '0']
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.inHand('Silver'))
        self.assertEqual(self.g.trashSize(), tsize + 2)

    def test_trash_little(self):
        """ Play a trading post but don't trash enough """
        tsize = self.g.trashSize()
        self.plr.test_input = ['1', '0']
        self.plr.playCard(self.card)
        self.assertFalse(self.plr.inHand('Silver'))
        self.assertEqual(self.g.trashSize(), tsize + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
