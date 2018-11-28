#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Lackeys(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'renaissance'
        self.name = 'Lackeys'
        self.cards = 2
        self.cost = 2

    ###########################################################################
    def desc(self, player):
        if player.phase == "buy":
            return "+2 Cards; When you gain this, +2 Villagers."
        else:
            return "+2 Cards"

    ###########################################################################
    def hook_gainThisCard(self, game, player):
        player.gainVillager(2)


###############################################################################
class Test_Lackeys(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Lackeys'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_playCard(self):
        self.card = self.g['Lackeys'].remove()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 7)
        self.assertLessEqual(self.plr.getVillager(), 0)

    def test_gainCard(self):
        self.plr.gainCard('Lackeys')
        self.assertLessEqual(self.plr.getVillager(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF