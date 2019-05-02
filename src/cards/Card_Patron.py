#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Patron(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reaction']
        self.base = 'renaissance'
        self.desc = "+1 Villager; +2. When something causes you to reveal this, +1 Coffers."
        self.name = 'Patron'
        self.cost = 4
        self.coin = 2

    def special(self, game, player):
        player.gainVillager(1)

    def hook_revealThisCard(self, game, player):
        player.gainCoffer()


###############################################################################
class Test_Patron(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Patron'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Patron'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.getVillager(), 1)

    def test_reveal(self):
        self.plr.revealCard(self.card)
        self.assertEqual(self.plr.getCoffer(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
