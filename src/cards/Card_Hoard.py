#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Hoard(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "Gain gold if buy victory"
        self.name = 'Hoard'
        self.playable = False
        self.gold = 2
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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['hoard'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['hoard'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getGold(), 2)
        self.assertEqual(self.plr.discardpile, [])

    def test_buy_victory(self):
        self.plr.playCard(self.card)
        self.plr.buyCard('estate')
        self.assertEqual(len(self.plr.discardpile), 2)
        for c in self.plr.discardpile:
            if c.name == 'Gold':
                break
        else:   # pragma: no cover
            self.fail("Didn't pickup gold")

    def test_buy_nonvictory(self):
        self.plr.playCard(self.card)
        self.plr.buyCard('copper')
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(self.plr.discardpile[-1].name, 'Copper')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
