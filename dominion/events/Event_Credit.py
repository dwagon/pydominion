#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Credit"""
import unittest

from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Credit(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "Gain an Action or Treasure costing up to $8. +Debt equal to its cost."
        self.name = "Credit"
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Gain an Action or Treasure costing up to $8. +Debt equal to its cost."""
        if card := player.plr_gain_card(8, types={Card.CardType.ACTION: True, Card.CardType.TREASURE: True}):
            player.debt.add(card.cost)


###############################################################################
class TestCredit(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Credit"], badcards=["Gold Mine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Credit"]

    def test_play(self) -> None:
        """No actions in play"""
        self.plr.coins.set(2)
        self.plr.test_input = ["Get Gold"]
        self.plr.perform_event(self.card)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.debt.get(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
