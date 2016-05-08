#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Alms(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.desc = "If you have no treasures in play, gain a card costing up to 4"
        self.name = "Alms"
        self.cost = 0

    def special(self, game, player):
        """ Once per turn: If you have no treasures in play, gain a
        card costing up to 4"""
        if not player.do_once('alms'):
            player.output("Already used Alms this turn")
            return
        found = False
        for c in player.played:
            if c.isTreasure():
                found = True
        for c in player.hand:
            if c.isTreasure():
                found = True
        if not found:
            if c.isTreasure():
                found = True
            player.plrGainCard(4)


###############################################################################
class Test_Alms(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['alms'], initcards=['feast'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g.events['Alms']

    def test_with_treasure(self):
        """ Use Alms with treasures"""
        self.plr.setHand('copper')
        self.plr.performEvent(self.card)

    def test_without_treasure(self):
        """ Use Alms with no treasures"""
        self.plr.setHand('estate')
        self.plr.test_input = ['feast']
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.discardpile[0].name, 'Feast')

    def test_twice(self):
        """ Use Alms twice"""
        self.plr.setHand('estate')
        self.plr.test_input = ['feast']
        self.plr.performEvent(self.card)
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.discardpile[0].name, 'Feast')
        self.assertEqual(self.plr.discardSize(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
