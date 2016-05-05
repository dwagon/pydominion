#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Treasurehunter(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'traveller']
        self.base = 'adventure'
        self.desc = "+1 Action, +1 Coin; Gain Silvers. Discard to replace with Warrior"
        self.name = 'Treasure Hunter'
        self.purchasable = False
        self.action = 1
        self.coins = 1
        self.cost = 3

    def special(self, game, player):
        """ Gain a Silver per card the player to your right gained in his last turn """
        pass    # TODO

    def hook_discardCard(self, game, player):
        """ Replace with Warrior """
        player.replace_traveller(self, 'Warrior')


###############################################################################
class Test_Treasurehunter(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['page'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['treasurehunter'].remove()

    def test_treasure_hunter(self):
        """ Play a treasure_hunter """
        pass


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
