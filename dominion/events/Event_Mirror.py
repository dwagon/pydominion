#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Mirror"""

import unittest
from typing import Any

from dominion import Game, Event, Piles, Card, OptionKeys, Player, PlayArea

MIRROR = "mirror"


###############################################################################
class Event_Mirror(Event.Event):
    """Mirror"""

    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+1 Buy; The next time you gain an Action card this turn, gain a copy of it."""
        self.name = "Mirror"
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.buys += 1

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if not card.isAction():
            return {}
        if player.do_once(MIRROR):
            player.gain_card(card.name)
        return {}


###############################################################################
class TestMirror(unittest.TestCase):
    """Test Mirror"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            events=["Mirror"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Mirror"]

    def test_play(self) -> None:
        """Perform a Mirror"""
        self.plr.coins.add(3)
        buys = self.plr.buys.get()
        self.plr.perform_event(self.event)
        self.plr.gain_card("Moat")
        self.assertEqual(self.plr.buys.get(), buys)  # -1 for performing event
        self.assertEqual(self.plr.piles[Piles.DISCARD].count("Moat"), 2)

    def test_non_action(self) -> None:
        """Test mirror when gaining a non-action card"""
        self.plr.coins.add(3)
        buys = self.plr.buys.get()
        self.plr.perform_event(self.event)
        self.plr.gain_card("Silver")
        self.assertEqual(self.plr.buys.get(), buys)  # -1 for performing event
        self.assertEqual(self.plr.piles[Piles.DISCARD].count("Silver"), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
