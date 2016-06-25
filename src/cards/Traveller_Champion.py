#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Champion(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'adventure'
        self.desc = "For the rest of the game +1 Action / Action; Defense"
        self.name = 'Champion'
        self.permanent = True
        self.purchasable = False
        self.defense = True
        self.numcards = 5
        self.cost = 6

    def special(self, game, player):
        """ For the rest of the game, when another player plays an Attack,
            it doesn't affect you, and when you play an Action, +1 Action. """
        pass

    def hook_postAction(self, game, player):
        player.addActions(1)


###############################################################################
class Test_Champion(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Page', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Champion'].remove()

    def test_champion(self):
        """ Play a champion """
        self.plr.addCard(self.card, 'duration')
        self.assertEqual(self.plr.getActions(), 1)
        moat = self.g['Moat'].remove()
        self.plr.addCard(moat, 'hand')
        self.plr.playCard(moat)
        self.assertEqual(self.plr.getActions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
