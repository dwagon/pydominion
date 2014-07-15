#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Shantytown(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+2 actions. If no action in hand, +2 cards"
        self.name = 'Shanty Town'
        self.actions = 2
        self.cost = 3

    def special(self, game, player):
        """ Reveal your hand. If you have no Action cards in hand, +2 cards"""
        for c in player.hand:
            if c.isAction():
                break
        else:
            player.pickupCards(2)


###############################################################################
class Test_Shantytown(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['shantytown', 'moat'])
        self.plr = list(self.g.players.values())[0]
        self.card = self.g['shantytown'].remove()

    def test_no_actions(self):
        """ Test Shany Town with no actions"""
        self.plr.setHand('estate', 'estate', 'gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.handSize(), 3 + 2)

    def test_actions(self):
        """ Test Shany Town with actions"""
        self.plr.setHand('moat', 'estate', 'gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.handSize(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
