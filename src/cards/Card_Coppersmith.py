#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Coppersmith(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "Copper produces an extra +1 this turn"
        self.name = 'Coppersmith'
        self.cost = 4

    def hook_spendValue(self, game, player, card):
        """ Copper produces an extra 1 this turn """
        if card.name == 'Copper':
            player.output("Copper worth 1 more")
            return 1
        return 0


###############################################################################
class Test_Coppersmith(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['coppersmith'])
        self.plr = list(self.g.players.values())[0]
        self.card = self.g['coppersmith'].remove()

    def test_copper(self):
        """ Copper should be worth two """
        self.plr.setHand('copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.plr.playCard(self.plr.hand[0])
        self.assertEqual(self.plr.getCoin(), 2)

    def test_silver(self):
        """ Silver should be unchanged and worth two """
        self.plr.setHand('silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.plr.playCard(self.plr.hand[0])
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
