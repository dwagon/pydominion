#!/usr/bin/env python

import unittest

import dominion.Card as Card
from dominion import Game, Piles


###############################################################################
class Card_Menagerie(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """+1 Action. Reveal your hand. If there are no duplicate cards in it,
            +3 Cards. Otherwise, +1 Card."""
        self.name = "Menagerie"
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        hand = set()
        for card in player.piles[Piles.HAND]:
            player.reveal_card(card)
            hand.add(card.name)
        if len(hand) == player.piles[Piles.HAND].size():
            player.output("No duplicates - picking up 3 cards")
            player.pickup_cards(3)
        else:
            player.output("Duplicates - picking up 1 card")
            player.pickup_cards(1)


###############################################################################
class Test_Menagerie(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Menagerie"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Menagerie")

    def test_play_unique(self):
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)

    def test_play_non_unique(self):
        self.plr.piles[Piles.HAND].set("Copper", "Copper", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
