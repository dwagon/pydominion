#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Deliver"""

import unittest
from typing import Any

from dominion import Game, Event, Piles, Card, OptionKeys, Player, PlayArea

DELIVER = "deliver"


###############################################################################
class Event_Deliver(Event.Event):
    """Deliver"""

    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = (
            """+1 Buy; This turn, each time you gain a card, sets it aside, and put it into your hand at end of turn."""
        )
        self.name = "Deliver"
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.buys += 1

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if DELIVER not in player.specials:
            player.specials[DELIVER] = PlayArea.PlayArea([])
        player.specials[DELIVER].add(card)
        player.secret_count += 1
        return {OptionKeys.DONTADD: True}

    def hook_end_turn(self, game: Game.Game, player: Player.Player) -> None:
        for card in player.specials[DELIVER]:
            player.add_card(card, Piles.HAND)
            player.secret_count -= 1
        player.specials[DELIVER] = PlayArea.PlayArea([])


###############################################################################
class TestDeliver(unittest.TestCase):
    """Test Deliver"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            events=["Deliver"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Deliver"]

    def test_play(self) -> None:
        """Perform a Deliver"""
        self.plr.coins.add(2)
        buys = self.plr.buys.get()
        self.plr.perform_event(self.event)
        self.plr.gain_card("Moat")
        self.assertEqual(self.plr.buys.get(), buys)  # -1 for performing event
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])
        self.plr.end_turn()
        self.assertIn("Moat", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
