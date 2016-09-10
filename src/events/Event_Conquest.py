#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Conquest(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'empires'
        self.desc = "Gain 2 Silvers. +1 VP per Silver you've gained this turn."
        self.name = "Conquest"
        self.cost = 6

    def special(self, game, player):
        for i in range(2):
            player.gainCard('Silver')
        sc = 0
        for card in player.stats['gained']:
            if card.name == 'Silver':
                sc += 1
        player.output("Gained %d VP from Conquest" % sc)
        player.addScore('Conquest', sc)


###############################################################################
class Test_Conquest(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Conquest'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g.events['Conquest']

    def test_event(self):
        """ Use Conquest """
        self.plr.addCoin(6)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertEqual(self.plr.discardSize(), 2)
        self.assertEqual(self.plr.getScoreDetails()['Conquest'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
