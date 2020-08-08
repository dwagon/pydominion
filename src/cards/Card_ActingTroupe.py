#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_ActingTroupe(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.RENAISSANCE
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
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Acting Troupe'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_playCard(self):
        self.card = self.g['Acting Troupe'].remove()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertLessEqual(self.plr.getVillager(), 4)
        self.assertIsNotNone(self.g.in_trash('Acting Troupe'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
