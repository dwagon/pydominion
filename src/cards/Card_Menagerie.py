#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Menagerie(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'cornucopia'
        self.desc = """+1 Action. Reveal your hand. If there are no duplicate cards in it, +3 Cards. Otherwise, +1 Card."""
        self.name = 'Menagerie'
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        hand = set()
        for card in player.hand:
            player.revealCard(card)
            hand.add(card.name)
        if len(hand) == player.handSize():
            player.output("No duplicates - picking up 3 cards")
            player.pickupCards(3)
        else:
            player.output("Duplicates - picking up 1 card")
            player.pickupCards(1)


###############################################################################
class Test_Menagerie(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Menagerie'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Menagerie'].remove()

    def test_play_unique(self):
        self.plr.setHand('Copper', 'Estate', 'Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.handSize(), 6)

    def test_play_non_unique(self):
        self.plr.setHand('Copper', 'Copper', 'Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.handSize(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
