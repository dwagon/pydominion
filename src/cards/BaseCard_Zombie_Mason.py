#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Zombie_Mason(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'zombie']
        self.base = 'nocturne'
        self.desc = "Trash the top card of your deck. You may gain a card costing up to 1 more than it."
        self.name = 'Zombie Mason'
        self.cost = 3
        self.purchaseable = False
        self.numcards = 1

    def setup(self, game):
        game.trashpile.add(self)

    def special(self, game, player):
        pass    # TODO


###############################################################################
class Test_Zombie_Mason(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Zombie Mason', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Zombie Mason'].remove()

    def test_play_noactions(self):
        pass


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
