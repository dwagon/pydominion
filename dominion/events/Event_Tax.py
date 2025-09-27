#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Tax"""

import unittest
from typing import Any

from dominion import Card, Game, Event, OptionKeys, Player, Phase

TAX = "tax"


###############################################################################
class Event_Tax(Event.Event):
    """Tax"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Add 2 debt to a Supply pile."""
        self.name = "Tax"
        self.cost = 2

    def setup(self, game: "Game.Game") -> None:
        """Setup: Add 1D to each Supply pile."""
        game.specials[TAX] = {}
        for name, _ in game.get_card_piles():
            game.specials[TAX][name] = 1

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Add 2 debt to a supply pile."""
        options: list[tuple[str, str]] = []
        for pile in game.specials[TAX]:
            options.append((f"Select {pile}", pile))
        pile_name = player.plr_choose_options("Pick a Supply pile to add 2 debt to", *options)
        game.specials[TAX][pile_name] += 2

    def hook_any_gain_card(
        self, game: "Game.Game", player: "Player.Player", card: "Card.Card"
    ) -> dict[OptionKeys, Any]:
        """When a player gains a card in their Buy phase, they take the D from its pile."""
        if game.specials[TAX].get(card.pile):
            game.specials[TAX][card.pile] -= 1
            player.debt.add(1)
        return {}

    def hook_all_card_description(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> str:
        if tax := game.specials[TAX].get(card.pile):
            if player.phase == Phase.BUY:
                return f"[Tax: {tax} Debt]"
        return ""


###############################################################################
class TestTax(unittest.TestCase):
    """Test Tax"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Tax"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Tax"]
        self.card = self.g.get_card_from_pile("Moat")

    def test_setup(self):
        """Perform a Tax"""
        self.assertEqual(self.g.specials[TAX]["Moat"], 1)

    def test_gain_card(self):
        """Gain a card"""
        debt = self.plr.debt.get()
        tax = self.g.specials[TAX]["Moat"]
        self.plr.gain_card("Moat")
        self.assertEqual(self.plr.debt.get(), debt + 1)
        self.assertEqual(self.g.specials[TAX]["Moat"], tax - 1)

    def test_play_event(self):
        """Play Event"""
        tax = self.g.specials[TAX]["Moat"]
        self.plr.coins.add(2)
        self.plr.test_input = ["Select Moat"]
        self.plr.perform_event(self.event)
        self.assertEqual(self.g.specials[TAX]["Moat"], tax + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
