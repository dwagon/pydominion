#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Receive_Tribute"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Receive_Tribute(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """If you've gained at least 3 cards this turn,
        gain up to 3 differently named Action cards you don't have copies of in play."""
        self.name = "Receive Tribute"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """If you've gained at least 3 cards this turn,
        gain up to 3 differently named Action cards you don't have copies of in play."""
        num_gained = len(player.stats["gained"])
        if num_gained < 3:
            player.output(f"You haven't gained enough cards - only {num_gained}")
            return
        selected: set[str] = set()
        for _ in range(3):
            choices: list[tuple[str, Any]] = [
                (f"Gain {card}", card)
                for card in game.get_action_piles(999)
                if card not in player.piles[Piles.PLAYED] and card not in selected
            ]
            choices.insert(0, ("Gain nothing", None))
            if choice := player.plr_choose_options("Gain a card", *choices):
                player.gain_card(choice)
                selected.add(choice)
            else:
                break


###############################################################################
class TestReceive_Tribute(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            events=["Receive Tribute"],
            initcards=["Moat", "Forge"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Receive Tribute"]

    def test_not_enough_cards(self) -> None:
        self.plr.stats["gained"] = [self.g.get_card_from_pile("Copper")]
        self.plr.coins.set(5)
        self.plr.perform_event(self.card)
        self.assertIn("You haven't gained enough cards - only 1", self.plr.messages)

    def test_enough_cards(self) -> None:
        self.plr.stats["gained"] = [
            self.g.get_card_from_pile("Copper"),
            self.g.get_card_from_pile("Copper"),
            self.g.get_card_from_pile("Copper"),
        ]
        self.plr.coins.set(5)
        self.plr.test_input = ["Gain Moat", "Gain Forge", "Gain nothing"]
        self.plr.perform_event(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertIn("Forge", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
