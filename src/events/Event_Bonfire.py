#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Bonfire(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.desc = "Trash up to two cards you have in play"
        self.name = "Bonfire"
        self.cost = 3

    def special(self, game, player):
        """ Trash up to two cards you have in play """
        player.plrTrashCard(num=2, cardsrc='played')


###############################################################################
class Test_Bonfire(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['bonfire'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g.events['Bonfire']
        self.copper = self.g['copper'].remove()
        self.gold = self.g['gold'].remove()
        self.estate = self.g['estate'].remove()

    def test_bonfire(self):
        """ Use Bonfire """
        self.plr.addCoin(3)
        self.plr.setHand('estate')
        self.plr.addCard(self.copper, 'hand')
        self.plr.playCard(self.copper)
        self.plr.addCard(self.gold, 'hand')
        self.plr.playCard(self.gold)
        self.plr.test_input = ['copper', 'gold', 'finish']
        self.plr.performEvent(self.card)
        self.assertEqual(self.g.trashSize(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
