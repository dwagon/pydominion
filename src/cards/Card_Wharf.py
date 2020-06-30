#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Wharf(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'seaside'
        self.desc = "+2 cards, +1 buy; next turn +2 cards, +1 buy"
        self.name = 'Wharf'
        self.cards = 2
        self.buys = 1
        self.cost = 5

    def duration(self, game, player):
        """ +2 card, +1 buy"""
        player.pickupCards(2)
        player.addBuys(1)


###############################################################################
class Test_Wharf(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Wharf'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.card = self.g['Wharf'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a wharf """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.handSize(), 7)
        self.assertEqual(self.plr.durationSize(), 1)
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertEqual(self.plr.durationSize(), 0)
        self.assertEqual(self.plr.playedSize(), 1)
        self.assertEqual(self.plr.played[-1].name, 'Wharf')
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.handSize(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
