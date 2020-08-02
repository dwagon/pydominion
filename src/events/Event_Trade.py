#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Trade(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.desc = "Trash up to 2 cards from your hand (not played); Gain a silver per trashed"
        self.name = "Trade"
        self.cost = 5

    def special(self, game, player):
        """ Trash up to 2 cards from your hand. Gain a Silver per card you trashed """
        trash = player.plrTrashCard(num=2)
        for _ in trash:
            player.gainCard('Silver')


###############################################################################
class Test_Trade(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Trade'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events['Trade']

    def test_play(self):
        """ Perform a Trade """
        self.plr.addCoin(5)
        self.plr.setHand('Copper', 'Estate', 'Gold')
        self.plr.test_input = ['copper', 'estate', 'finish']
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.discardSize(), 2)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Silver')
        self.assertIsNone(self.plr.inHand('Copper'))
        self.assertIsNone(self.plr.inHand('Estate'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
