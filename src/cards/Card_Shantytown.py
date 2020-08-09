#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Shantytown(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.INTRIGUE
        self.desc = "+2 actions. If no action in hand, +2 cards"
        self.name = 'Shanty Town'
        self.actions = 2
        self.cost = 3

    def special(self, game, player):
        """ Reveal your hand. If you have no Action cards in hand, +2 cards"""
        for c in player.hand:
            player.revealCard(c)
            if c.isAction():
                break
        else:
            player.output("No actions - picking up 2 cards")
            player.pickupCards(2)


###############################################################################
class Test_Shantytown(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Shanty Town', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Shanty Town'].remove()

    def test_no_actions(self):
        """ Test Shany Town with no actions"""
        self.plr.setHand('Estate', 'Estate', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.handSize(), 3 + 2)

    def test_actions(self):
        """ Test Shany Town with actions"""
        self.plr.setHand('Moat', 'Estate', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.handSize(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
