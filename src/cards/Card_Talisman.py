#!/usr/bin/env python

import unittest
from Card import Card


class Card_Talisman(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'prosperity'
        self.desc = "+1 gold. Gain copy of non-victory cards you buy"
        self.name = 'Talisman'
        self.playable = False
        self.cost = 4
        self.gold = 1

    def hook_buyCard(self, game, player, card):
        """ While this is in play, when you buy a card costing 4
            or less that is not a victory card, gain a copy of it."""
        if card.cost <= 4 and not card.isVictory():
            player.output("Gained another %s from Talisman" % card.name)
            player.addCard(game[card.cardname].remove())


###############################################################################
class Test_Talisman(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['talisman'])
        self.plr = self.g.players[0]
        self.card = self.g['talisman'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.t['gold'], 1)

    def test_buy(self):
        self.plr.playCard(self.card)
        self.plr.buyCard('copper')
        self.assertEqual(len(self.plr.discardpile), 2)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Copper')

    def test_tooexpensive(self):
        self.plr.playCard(self.card)
        self.plr.buyCard('gold')
        self.assertEqual(len(self.plr.discardpile), 1)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Gold')

    def test_victory(self):
        self.plr.playCard(self.card)
        self.plr.buyCard('duchy')
        self.assertEqual(len(self.plr.discardpile), 1)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Duchy')
        
        

###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF
