#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Hoard(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+2 coin; While this is in play, when you buy a Victory card, gain a Gold"
        self.name = 'Hoard'
        self.playable = False
        self.coin = 2
        self.cost = 6

    def hook_buyCard(self, game, player, card):
        """ When this is in play, when you buy a Victory card, gain a Gold """
        if card.isVictory():
            player.output("Gaining Gold from Hoard")
            player.addCard(game['Gold'].remove())


###############################################################################
class Test_Hoard(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Hoard'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Hoard'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertTrue(self.plr.discardpile.isEmpty())

    def test_buy_victory(self):
        self.plr.playCard(self.card)
        self.plr.buyCard(self.g['Estate'])
        self.assertEqual(self.plr.discardSize(), 2)
        for c in self.plr.discardpile:
            if c.name == 'Gold':
                break
        else:   # pragma: no cover
            self.fail("Didn't pickup gold")

    def test_buy_nonvictory(self):
        self.plr.playCard(self.card)
        self.plr.buyCard(self.g['Copper'])
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertEqual(self.plr.discardpile[-1].name, 'Copper')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
