#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Alms(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.name = "Alms"
        self.cost = 0

    def desc(self, player):
        if self.treasures(player):
            return "You have treasures in play so you can't gain a card costing up to 4"
        else:
            return "You have no treasures in play, gain a card costing up to 4"

    def treasures(self, player):
        t = 0
        t += sum([1 for c in player.played if c.isTreasure()])
        t += sum([1 for c in player.hand if c.isTreasure()])
        return t

    def special(self, game, player):
        """ Once per turn: If you have no treasures in play, gain a
        card costing up to 4"""
        if not player.do_once('Alms'):
            player.output("Already used Alms this turn")
            return

        if self.treasures(player) == 0:
            player.plrGainCard(4)


###############################################################################
class Test_Alms(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Alms'], initcards=['Feast'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events['Alms']

    def test_with_treasure(self):
        """ Use Alms with treasures"""
        self.plr.setHand('Copper')
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.discardSize(), 0)

    def test_without_treasure(self):
        """ Use Alms with no treasures"""
        self.plr.setHand('Estate')
        self.plr.test_input = ['Feast']
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertEqual(self.plr.discardpile[0].name, 'Feast')

    def test_twice(self):
        """ Use Alms twice"""
        self.plr.setHand('Estate')
        self.plr.test_input = ['feast']
        self.plr.performEvent(self.card)
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertEqual(self.plr.discardpile[0].name, 'Feast')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
