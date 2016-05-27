#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Ball(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.desc = "Take -1 Coin token; Gain 2 cards each costing up to 4 Coin"
        self.name = "Ball"
        self.cost = 5

    def special(self, game, player):
        player.coin_token = True
        for i in range(2):
            player.plrGainCard(cost=4)


###############################################################################
class Test_Ball(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Ball'], initcards=['Militia', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g.events['Ball']

    def test_ball(self):
        """ Use Ball """
        self.plr.addCoin(5)
        self.plr.test_input = ['militia', 'moat']
        self.plr.performEvent(self.card)
        self.assertTrue(self.plr.coin_token)
        self.assertIsNotNone(self.plr.inDiscard('Militia'))
        self.assertIsNotNone(self.plr.inDiscard('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
