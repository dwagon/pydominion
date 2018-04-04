#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Masterpiece(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'guilds'
        self.name = 'Masterpiece'
        self.overpay = True
        self.coin = 1
        self.cost = 3

    def desc(self, player):
        if player.phase == "buy":
            return "+1 Coin. When you buy this, you may overpay for it. If you do, gain a Silver per coin you overpaid."
        else:
            return "+1 Coin"

    def hook_overpay(self, game, player, amount):
        player.output("Gained %d Silvers" % amount)
        for i in range(amount):
            player.gainCard('Silver')


###############################################################################
class Test_Masterpiece(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Masterpiece'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Masterpiece'].remove()

    def test_play(self):
        """ Play a Masterpiece """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_buy(self):
        """ Buy a Masterpiece """
        self.plr.coin = 5
        self.plr.test_input = ['1']
        self.plr.buyCard(self.g['Masterpiece'])
        self.assertIsNotNone(self.plr.inDiscard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
