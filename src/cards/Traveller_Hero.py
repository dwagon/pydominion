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
        self.coins = 2
        self.cost = 5

    def special(self, game, player):
        """ Gain a treasure """
        pass    # TODO

    def hook_discardCard(self, game, player):
        """ Replace with Champion """
        player.replace_traveller(self, 'Champion')


###############################################################################
class Test_Hero(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Page'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Hero'].remove()

    def test_hero(self):
        """ Play a hero """
        pass


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
