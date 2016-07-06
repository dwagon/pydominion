#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_Capital(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'empires'
        self.desc = "6 Coin +1 Buy. When you discard this from play, take 6 Debt, and then you may pay off Debt"
        self.name = 'Capital'
        self.coin = 6
        self.buys = 1
        self.cost = 5

    def hook_discardCard(self, game, player):
        player.debt += 6
        player.payback()


###############################################################################
class Test_Capital(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Capital'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Capital'].remove()

    def test_play(self):
        """ Play a Capital """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.getBuys(), 2)
        self.assertEquals(self.plr.getCoin(), 6)
        self.plr.coin = 3
        self.plr.discardCard(self.card)
        self.assertEqual(self.plr.debt, 3)
        self.assertEqual(self.plr.coin, 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
