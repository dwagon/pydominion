#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_SaltEarth(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'empires'
        self.desc = "+1VP. Trash a Victory card from the Supply."
        self.name = "Salt the Earth"
        self.cost = 4

    def special(self, game, player):
        player.addScore('Salt the Earth', 1)
        stacks = game.getVictoryPiles()
        cp = player.cardSel(cardsrc=stacks, prompt="Trash a Victory card from the Supply")
        if not cp:
            return
        cd = cp[0].remove()
        player.trashCard(cd)


###############################################################################
class Test_SaltEarth(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Salt the Earth'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.event = self.g.events['Salt the Earth']

    def test_event(self):
        """ Use Salt the Earth"""
        self.plr.addCoin(4)
        self.plr.test_input = ['Province']
        self.plr.performEvent(self.event)
        self.assertEqual(self.plr.getScoreDetails()['Salt the Earth'], 1)
        self.assertIsNotNone(self.g.inTrash('Province'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
