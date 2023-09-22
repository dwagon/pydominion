#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Madman(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+2 Actions. Return this to the Madman pile. If you do, +1 Card per card in your hand."""
        self.name = "Madman"
        self.insupply = False
        self.actions = 2
        self.cost = 0
        self.purchasable = False

    def special(self, game, player):
        handsize = player.piles[Piles.HAND].size()
        player.output(f"Gaining {handsize} cards from madman")
        for _ in range(handsize):
            player.pickup_card()
        game.card_piles["Madman"].add(self)
        player.piles[Piles.PLAYED].remove(self)


###############################################################################
class TestMadman(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Hermit"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Madman")

    def test_play(self):
        """Play a Madman"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 * 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
