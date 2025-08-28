#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Deliver"""

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
            player.specials[DELIVER] = PlayArea.PlayArea(initial=[])
        if card.location == Piles.SPECIAL:  # Already added
            return {}
        player.specials[DELIVER].add(card)
        card.location = Piles.SPECIAL
        player.secret_count += 1
        return {OptionKeys.DONTADD: True}

    def hook_end_turn(self, game: Game.Game, player: Player.Player) -> None:
        if DELIVER in player.specials:
            for card in player.specials[DELIVER]:
                player.output(f"Deliver putting {card} back into hand")
                player.add_card(card, Piles.HAND)
                player.secret_count -= 1
        player.specials[DELIVER] = PlayArea.PlayArea(initial=[])


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

    def test_twice(self) -> None:
        """Perform Deliver twice"""
        self.plr.coins.add(4)
        buys = self.plr.buys.get()
        self.plr.perform_event(self.event)
        self.plr.perform_event(self.event)
        self.plr.gain_card("Moat")
        self.assertEqual(self.plr.buys.get(), buys)
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])
        self.assertEqual(len(self.plr.specials[DELIVER]), 1, "Only gets added to specials once")
        self.plr.end_turn()
        self.assertIn("Moat", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
