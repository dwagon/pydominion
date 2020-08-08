#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Populate(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'menagerie'
        self.desc = "Gain one card from each Action Supply pile."
        self.name = "Populate"
        self.cost = 10

    def special(self, game, player):
        for cp in game.cardpiles.values():
            if cp.isAction() and cp.insupply:
                player.output("Gained {} from Populate".format(cp.name))
                player.gainCard(cp)


###############################################################################
class Test_Populate(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, eventcards=['Populate'],
            initcards=['Moat'], badcards=['Hostelry', 'Border Village', 'Inn']
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events['Populate']

    def test_Populate(self):
        """ Use Populate """
        self.plr.addCoin(10)
        self.plr.performEvent(self.card)
        self.g.print_state()
        self.assertIsNotNone(self.plr.in_discard('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
