#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Piles, OptionKeys, Card, Player


###############################################################################
class Card_Scheme(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """+1 Card +1 Action; At the start of Clean-up this turn,
            you may choose an Action card you have in play. If you discard it from play
            this turn, put it on your deck."""
        self.name = "Scheme"
        self.cards = 1
        self.actions = 1
        self.cost = 3

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        actions = [c for c in player.piles[Piles.PLAYED] if c.isAction()]
        if card := player.card_sel(cardsrc=actions, prompt="Select an action to put back on your deck"):
            player.add_card(card[0], Piles.TOPDECK)
            player.piles[Piles.PLAYED].remove(card[0])
        return {}


###############################################################################
class Test_Scheme(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Scheme", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Scheme")

    def test_play(self) -> None:
        """Play a scheme"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.PLAYED].set("Moat")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)
        self.plr.test_input = ["moat"]
        self.plr.cleanup_phase()
        self.assertIn("Moat", self.plr.piles[Piles.HAND])
        self.assertIn("Scheme", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
