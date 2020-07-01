#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Spoils(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'darkages'
        self.desc = "+3 coin. When you play this, return it to the Spoils pile."
        self.basecard = True
        self.purchasable = False
        self.name = 'Spoils'
        self.cost = 0
        self.coin = 3
        self.numcards = 15

    def special(self, player, game):
        """ When you play this return it to the spoils pile """
        game['Spoils'].add()
        player.played.remove(self)


###############################################################################
class Test_Spoils(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bandit Camp'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        numspoils = self.g['Spoils'].numcards
        spoils = self.g['Spoils'].remove()
        self.plr.addCard(spoils, 'hand')
        self.plr.playCard(spoils)
        self.assertEqual(self.plr.getCoin(), 3)
        self.assertTrue(self.plr.played.isEmpty())
        self.assertEqual(self.g['Spoils'].numcards, numspoils)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
