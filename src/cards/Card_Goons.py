#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Goons(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "Other players discard down to 3. +1 VP when buying"
        self.name = 'Goons'
        self.cost = 6
        self.buy = 1
        self.coin = 2

    def special(self, game, player):
        """ Each other player discards down to three cards """
        for plr in player.attackVictims():
            plr.output("Discard down to 3 cards")
            plr.plrDiscardDownTo(3)

    def hook_buyCard(self, game, player, card):
        """ While this card is in play, when you buy a card +1 VP """
        player.output("Scored 1 more from goons")
        player.addScore('Goons', 1)


###############################################################################
class Test_Goons(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['goons', 'moat'])
        self.plr, self.victim = self.g.playerList()
        self.card = self.g['goons'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.victim.test_input = ['1', '2', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.victim.handSize(), 3)

    def test_defended(self):
        self.victim.setHand('moat', 'estate', 'gold', 'copper')
        self.plr.playCard(self.card)
        self.assertEqual(self.victim.handSize(), 4)

    def test_buy(self):
        self.victim.setHand('moat', 'estate', 'gold', 'copper')
        self.plr.playCard(self.card)
        self.plr.buyCard('copper')
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Goons'], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
