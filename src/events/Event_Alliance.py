#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Alliance(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "Gain a Province, a Duchy, an Estate, a Gold, a Silver, and a Copper."
        self.name = "Alliance"
        self.cost = 10

    def special(self, game, player):
        player.gainCard('Province')
        player.gainCard('Duchy')
        player.gainCard('Estate')
        player.gainCard('Gold')
        player.gainCard('Silver')
        player.gainCard('Copper')


###############################################################################
class Test_Alliance(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Alliance'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.events['Alliance']

    def test_play(self):
        """ Perform a Alliance """
        self.plr.addCoin(10)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_discard('Province'))
        self.assertIsNotNone(self.plr.in_discard('Gold'))
        self.assertIsNotNone(self.plr.in_discard('Copper'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
