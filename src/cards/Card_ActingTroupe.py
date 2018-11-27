#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_ActingTroupe(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'renaissance'
        self.name = 'Acting Troupe'
        self.desc = "+4 Villagers. Trash this."
        self.cost = 3

    ###########################################################################
    def special(self, game, player):
        player.gainVillager(4)
        player.trashCard(self)


###############################################################################
class Test_ActingTroupe(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Acting Troupe'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_playCard(self):
        self.card = self.g['Acting Troupe'].remove()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertLessEqual(self.plr.getVillager(), 4)
        self.assertIsNotNone(self.g.inTrash('Acting Troupe'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
