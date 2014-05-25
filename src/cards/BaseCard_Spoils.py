#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Spoils(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'darkages'
        self.desc = "+3 gold - once off"
        self.basecard = True
        self.purchasable = False
        self.name = 'Spoils'
        self.cost = 0
        self.gold = 3

    def special(self, player, game):
        """ When you play this return it to the spoils pile """
        game['Spoils'].add()
        player.played.remove(self)


###############################################################################
class Test_Spoils(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['banditcamp'])
        self.plr = self.g.players[0]

    def test_play(self):
        numspoils = self.g['Spoils'].numcards
        spoils = self.g['Spoils'].remove()
        self.plr.addCard(spoils, 'hand')
        self.plr.spendCard(spoils)
        self.assertEqual(self.plr.t['gold'], 3)
        self.assertEqual(self.plr.played, [])
        self.assertEqual(self.g['Spoils'].numcards, numspoils)


###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF
