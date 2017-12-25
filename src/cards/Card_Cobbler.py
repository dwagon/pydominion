#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Cobbler(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night', 'duration']
        self.base = 'nocturne'
        self.desc = "At the start of your next turn, gain a card to your hand costing up to 4."
        self.name = 'Cobbler'
        self.cost = 5

    def duration(self, game, player):
        player.plrGainCard(4)


###############################################################################
class Test_Cobbler(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cobbler'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Cobbler'].remove()

    def test_duration(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.plr.endTurn()
        self.plr.test_input = ['1']
        self.plr.startTurn()
        self.assertLessEqual(self.plr.discardpile[0].cost, 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF