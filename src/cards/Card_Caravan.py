#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Caravan(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'seaside'
        self.desc = "+1 cards, +1 action; +1 card next turn"
        self.name = 'Caravan'
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def duration(self, game, player):
        """ +1 card next turn"""
        player.pickupCards(1, verb="Picked up from Caravan:")


###############################################################################
class Test_Caravan(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Caravan'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Caravan'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a caravan """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.durationSize(), 1)
        self.plr.end_turn()
        self.plr.startTurn()
        self.assertEqual(self.plr.durationSize(), 0)
        self.assertEqual(self.plr.playedSize(), 1)
        self.assertEqual(self.plr.played[-1].name, 'Caravan')
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
