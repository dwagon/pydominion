#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Commerce(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "Gain a Gold per differently named card you've gained this turn."
        self.name = "Commerce"
        self.cost = 5

    def special(self, game, player):
        gains = {_.name for _ in player.stats['gained']}
        for _ in gains:
            player.gainCard('Gold')


###############################################################################
class Test_Commerce(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Commerce'], initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events['Commerce']

    def test_Commerce(self):
        """ Use Commerce """
        self.plr.addCoin(5)
        self.plr.gainCard('Moat')
        self.plr.performEvent(self.card)
        self.g.print_state()
        self.assertIsNotNone(self.plr.in_discard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
