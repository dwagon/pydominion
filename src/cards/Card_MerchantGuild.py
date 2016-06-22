#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_MerchantGuild(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'guilds'
        self.desc = """+1 Buy +1 Coin. While this is in play, when you buy a card, take a Coin token."""
        self.name = 'Merchant Guild'
        self.coin = 1
        self.buys = 1
        self.cost = 5

    def hook_buyCard(self, game, player, card):
        player.output("Gaining Coin token from Merchant Guild")
        player.gainSpecialCoins()


###############################################################################
class Test_MerchantGuild(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Merchant Guild'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Merchant Guild'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the card """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_buy(self):
        """ Play the card """
        self.plr.playCard(self.card)
        self.plr.buyCard(self.g['Estate'])
        self.assertEqual(self.plr.getSpecialCoins(), 1)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
