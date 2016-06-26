#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_NomadCamp(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'hinterlands'
        self.desc = "+1 Buy +2 Coins; When you gain this, put it on top of your deck."
        self.name = 'Nomad Camp'
        self.buys = 1
        self.cards = 2
        self.cost = 4

    def hook_gainThisCard(self, game, player):
        return {'destination': 'topdeck'}


###############################################################################
class Test_NomadCamp(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Nomad Camp'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Nomad Camp'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 7)
        self.assertEqual(self.plr.getBuys(), 2)

    def test_gain(self):
        self.plr.gainCard('Nomad Camp')
        self.assertEqual(self.plr.deck[-1].name, 'Nomad Camp')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF