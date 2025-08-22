#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Travelling_Fair"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Event, OptionKeys, Player


###############################################################################
class Event_TravellingFair(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+2 Buys; When you gain a card this turn, you may put it onto your deck."
        self.name = "Travelling Fair"
        self.cost = 2
        self.buys = 2

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        choice = player.plr_choose_options(
            f"Do you want to put {card} on the top of your deck?",
            (f"Put {card} on deck", Piles.TOPDECK),
            (f"Discard {card}", Piles.DISCARD),
        )
        return {OptionKeys.DESTINATION: choice}


###############################################################################
class TestTravellingFair(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Travelling Fair"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Travelling Fair"]

    def test_play_discard(self) -> None:
        """Perform a Travelling Fair"""
        self.plr.coins.add(2)
        self.plr.perform_event(self.card)
        self.plr.test_input = ["Discard"]
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Gold"])
        self.assertNotIn("Gold", self.plr.piles[Piles.DECK])

    def test_play_deck(self) -> None:
        """Perform a Travelling Fair and deck the card"""
        self.plr.coins.add(2)
        self.plr.perform_event(self.card)
        self.plr.test_input = ["Put"]
        self.plr.gain_card("Gold")
        self.g.print_state()
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
