#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Bonfire(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "Trash up to two cards you have in play"
        self.name = "Bonfire"
        self.cost = 3

    def special(self, game, player):
        """ Trash up to two cards you have in play """
        player.plrTrashCard(num=2, cardsrc='played')


###############################################################################
class Test_Bonfire(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Bonfire'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events['Bonfire']
        self.copper = self.g['Copper'].remove()
        self.gold = self.g['Gold'].remove()
        self.estate = self.g['Estate'].remove()

    def test_bonfire(self):
        """ Use Bonfire """
        tsize = self.g.trashSize()
        self.plr.addCoin(3)
        self.plr.setHand('Estate')
        self.plr.addCard(self.copper, 'hand')
        self.plr.playCard(self.copper)
        self.plr.addCard(self.gold, 'hand')
        self.plr.playCard(self.gold)
        self.plr.test_input = ['Copper', 'Gold', 'Finish']
        self.plr.performEvent(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
