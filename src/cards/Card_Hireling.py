#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Hireling(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'adventure'
        self.desc = "+1 Card forever"
        self.name = 'Hireling'
        self.cost = 6
        self.permanent = True

    def special(self, game, player):
        pass

    def duration(self, game, player):
        player.pickupCard()


###############################################################################
class Test_Hireling(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Hireling'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Hireling'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_hireling(self):
        """ Play a hireling """
        self.plr.playCard(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.handSize(), 6)
        self.assertIsNone(self.plr.in_discard('Hireling'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
