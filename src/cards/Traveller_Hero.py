#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Hero(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'traveller']
        self.base = 'adventure'
        self.desc = "+2 Coin, Gain a Treasure; Discard to replace with Champion"
        self.name = 'Hero'
        self.purchasable = False
        self.coin = 2
        self.cost = 5
        self.numcards = 5

    def special(self, game, player):
        """ Gain a treasure """
        player.plrGainCard(cost=None, types={'treasure': True})

    def hook_discardThisCard(self, game, player, source):
        """ Replace with Champion """
        player.replace_traveller(self, 'Champion')


###############################################################################
class Test_Hero(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Page'], badcards=["Fool's Gold"])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Hero'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_hero(self):
        """ Play a hero """
        self.plr.test_input = ['gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
