#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Amass(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "If you have no Action cards in play, gain an Action card costing up to $5."
        self.name = "Amass"
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """If you have no Action cards in play, gain an Action card costing up to $5."""
        if not [_ for _ in player.piles[Piles.PLAYED] if _.isAction()]:
            player.plr_gain_card(6, types={Card.CardType.ACTION: True})
        else:
            player.output("You have Action cards in play - no effect")


###############################################################################
class TestAmass(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            events=["Amass"],
            initcards=["Moat"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Amass"]

    def test_no_actions(self) -> None:
        """No actions in play"""
        self.plr.coins.set(2)
        self.plr.test_input = ["Get Moat"]
        self.plr.perform_event(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])

    def test_actions(self) -> None:
        """Actions in play"""
        self.plr.coins.set(2)
        self.plr.piles[Piles.PLAYED].set("Moat")
        self.plr.test_input = ["Get Moat"]
        self.plr.perform_event(self.card)
        self.assertNotIn("Moat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
