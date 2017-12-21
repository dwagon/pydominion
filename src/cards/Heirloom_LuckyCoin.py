#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_LuckyCoin(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['treasure', 'heirloom']
        self.base = 'nocturne'
        self.desc = "1 Coin; When you play this, gain a Silver."
        self.name = 'Lucky Coin'
        self.cost = 4
        self.coin = 1
        self.purchasable = False

    def special(self, game, player):
        player.gainCard('Silver')


###############################################################################
class Test_LuckyCoin(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Fool'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Lucky Coin'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.discardpile[0].name, 'Silver')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
