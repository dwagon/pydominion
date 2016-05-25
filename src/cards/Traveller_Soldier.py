#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Soldier(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'traveller']
        self.base = 'adventure'
        self.desc = """+2 Coins; +1 Coin per other Attack you have in play.
        Each other player with 4 or more cards in hand discards a card."""
        self.name = 'Soldier'
        self.purchasable = False
        self.coin = 2
        self.cost = 3

    def special(self, game, player):
        """+2 Coins; +1 Coin per other Attack you have in play.
        Each other player with 4 or more cards in hand discards a card."""
        count = 0
        for c in player.played:
            if c == self:
                continue
            if c.isAttack():
                count += 1
        player.addCoin(count)

    def hook_discardCard(self, game, player):
        """ Replace with Hero """
        player.replace_traveller(self, 'Fugitive')


###############################################################################
class Test_Soldier(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Peasant', 'Militia'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Soldier'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_soldier(self):
        """ Play a soldier with no extra attacks """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_soldier_more(self):
        """ Play a soldier with no extra attacks """
        mil = self.g['Militia'].remove()
        self.plr.addCard(mil, 'played')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
