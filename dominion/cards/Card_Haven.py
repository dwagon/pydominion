#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Haven(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = "+1 cards, +1 action; play a card next turn"
        self.name = "Haven"
        self.cards = 1
        self.actions = 1
        self.cost = 4
        self.savedHavenCard = None

    def special(self, game, player):
        """Set aside a card from your hand face down. At the start of
        your next turn, put it into your hand."""
        card = player.plr_pick_card(
            force=True, prompt="Pick card to put into hand next turn"
        )
        player.add_card(card, "duration")
        player.piles[Piles.HAND].remove(card)
        self.savedHavenCard = card

    def duration(self, game, player):
        card = self.savedHavenCard
        if not card:
            return
        player.move_card(card, Piles.HAND)
        player.output(f"Pulling {card} out of from haven")
        self.savedHavenCard = None


###############################################################################
class TestHaven(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Haven"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Haven")
        self.plr.piles[Piles.DISCARD].set(
            "Copper", "Copper", "Copper", "Copper", "Copper"
        )
        self.plr.piles[Piles.DECK].set("Estate", "Estate", "Estate", "Estate", "Gold")
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play a haven"""
        self.plr.test_input = ["select gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 2)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 1)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
