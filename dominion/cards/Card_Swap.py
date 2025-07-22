#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Swap(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALLIES
        self.cards = 1
        self.actions = 1
        self.name = "Swap"
        self.desc = """+1 Card; +1 Action; You may return an Action from your
            hand to its pile, to gain to your hand a different Action costing
            up to $5."""
        self.cost = 5

    def special(self, game, player):
        acts = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        if not acts:
            return
        if choice := player.card_sel(
            prompt="Pick a card to return to its pile to gain a different one costing up to $5",
            cardsrc=acts,
        ):
            player.piles[Piles.HAND].remove(choice[0])
            game.card_piles[choice[0].pile].add(choice[0])
            player.plr_gain_card(5, "less")


###############################################################################
class TestSwap(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Swap", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Swap")

    def test_play(self):
        """Play the card"""
        self.plr.piles[Piles.HAND].set("Moat", "Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Select Moat", "Get Swap"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2 + 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Swap", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
