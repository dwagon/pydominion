#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Windfall(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'empires'
        self.desc = "If your deck and discard pile are empty, gain 3 Golds"
        self.name = "Windfall"
        self.cost = 5

    def special(self, game, player):
        if player.deck.isEmpty() and player.discardpile.isEmpty():
            for i in range(3):
                player.gainCard('Gold')


###############################################################################
class Test_Windfall(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Windfall'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.card = self.g.events['Windfall']

    def test_play(self):
        """ Perform a Windfall """
        self.plr.addCoin(5)
        self.plr.setDiscard()
        self.plr.setDeck()
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.discardSize(), 3)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Gold')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
