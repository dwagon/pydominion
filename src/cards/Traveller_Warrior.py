#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Warrior(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'traveller']
        self.base = 'adventure'
        self.desc = "+2 Card; Attack; Discard to replace with Hero"
        self.name = 'Warrior'
        self.purchasable = False
        self.cards = 2
        self.cost = 4

    def special(self, game, player):
        """ For each Traveller you have in play (including this), each other
        player discards the top card of his deck and trashit it if it
        costs 3 or 4 """
        pass

    def hook_discardCard(self, game, player):
        """ Replace with Hero """
        player.replace_traveller(self, 'Hero')


###############################################################################
class Test_Warrior(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['page'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['warrior'].remove()

    def test_warrior(self):
        """ Play a warrior """
        pass


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
