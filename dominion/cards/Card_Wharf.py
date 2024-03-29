#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Wharf(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = "+2 cards, +1 buy; next turn +2 cards, +1 buy"
        self.name = "Wharf"
        self.cards = 2
        self.buys = 1
        self.cost = 5

    def duration(self, game, player):
        """+2 card, +1 buy"""
        player.pickup_cards(2)
        player.buys.add(1)


###############################################################################
class Test_Wharf(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wharf"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Wharf")
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play a wharf"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 0)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 1)
        self.assertEqual(self.plr.piles[Piles.PLAYED][-1].name, "Wharf")
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
