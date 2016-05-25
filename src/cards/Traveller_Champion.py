#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Champion(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'adventure'
        self.desc = "+1 Action / Action; Permanent Defense"
        self.name = 'Champion'
        self.cost = 6

    def special(self, game, player):
        """ For the rest of teh game, when another player plays an Attack,
            it doesn't affect you, and when you play an Action, +1 Action. """
        pass    # TODO


###############################################################################
class Test_Champion(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Page'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Champion'].remove()

    def test_champion(self):
        """ Play a champion """
        pass


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
