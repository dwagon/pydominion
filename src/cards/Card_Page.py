#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Page(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'traveller']
        self.base = 'adventure'
        self.desc = "+1 Card, +1 Action; Discard to replace with Treasure Hunter"
        self.name = 'Page'
        self.traveller = True
        self.cards = 1
        self.actions = 1
        self.cost = 2

    def hook_discardCard(self, game, player):
        """ Replace with Treasure Hunter """
        player.replace_traveller(self, 'TreasureHunter')


###############################################################################
class Test_Page(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['page'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['page'].remove()

    def test_page(self):
        """ Play a page """
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 1)
        self.assertEqual(self.plr.getActions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
