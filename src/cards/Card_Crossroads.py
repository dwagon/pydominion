#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Crossroads(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action']
        self.base = 'hinterlands'
        self.desc = "+1 card per victory card in hand, +3 actions first time"
        self.name = 'Crossroads'
        self.cost = 2

    ###########################################################################
    def special(self, game, player):
        """ Reveal your hand. +1 Card per Victory card revealed.
            If this is the first time you played a Crossroads this turn,
            +3 Actions """
        vict = sum([1 for c in player.hand if c.isVictory()])
        for i in range(vict):
            player.pickupCard()
        numcross = sum([1 for c in player.played if c.name == 'Crossroads'])
        if numcross == 1:
            player.addActions(3)


###############################################################################
class Test_Crossroads(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['crossroads'])
        self.plr = list(self.g.players.values())[0]
        self.card = self.g['crossroads'].remove()

    def test_play(self):
        """ Play crossroads once"""
        self.plr.setHand('silver', 'estate', 'estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.getActions(), 3)

    def test_play_twice(self):
        """ Play crossroads again """
        self.plr.setHand('silver', 'copper', 'crossroads')
        self.plr.setPlayed('crossroads')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
