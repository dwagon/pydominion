#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Shepherd(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'nocturne'
        self.desc = "+1 action; Discard any number of victory cards +2 cards per card discarded"
        self.name = 'Shepherd'
        self.cost = 2
        self.action = 1
        self.heirloom = 'Pasture'

    def special(self, game, player):
        pass
        # TODO


###############################################################################
class Test_Shepherd(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Shepherd'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Shepherd'].remove()

    def test_play(self):
        """ Play a Shepherd """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
