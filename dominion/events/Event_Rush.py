#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Rush"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, Event, Player, OptionKeys


###############################################################################
class Event_Rush(Event.Event):
    """Rush"""

    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = (
            """+1 Buy; The next time you gain an Action card this turn, play it."""
        )
        self.name = "Rush"
        self.cost = 2
        self.buys = 1

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if not card.isAction():
            return {}
        player.play_card(card, discard=False, cost_action=False)
        return {}


###############################################################################
class TestRush(unittest.TestCase):
    """Test Rush"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Rush"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Rush"]

    def test_rush(self) -> None:
        """Use Rush"""
        self.plr.coins.set(2)
        hand_size = len(self.plr.piles[Piles.HAND])
        buys = self.plr.buys.get()
        self.plr.perform_event(self.event)
        self.assertEqual(
            self.plr.buys.get(), buys
        )  # +1 for Rush, -1 for performing event
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.gain_card("Moat")
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
