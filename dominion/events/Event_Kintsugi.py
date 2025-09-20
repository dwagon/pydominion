#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Kintsugi(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """Trash a card from your hand. If you've gained a Gold this game, gain a card
            costing up to $2 more than the trashed card."""
        self.name = "Kintsugi"
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Trash a card from your hand. If you've gained a Gold this game, gain a card
        costing up to $2 more than the trashed card."""
        if card := player.plr_trash_card():
            # Should check if we ever have had a gold, rather than currently have Gold
            if "Gold" in player.all_cards():
                player.plr_gain_card(cost=card[0].cost + 2)


###############################################################################
class TestKintsugi(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            events=["Kintsugi"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Kintsugi"]

    def test_play_no_gold(self) -> None:
        """Use Kintsugi never having a Gold"""
        self.plr.coins.set(3)
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate", "Duchy")
        self.plr.test_input = ["Trash Copper"]
        self.plr.perform_event(self.card)
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])
        self.assertIn("Copper", self.g.trash_pile)

    def test_play_with_gold(self) -> None:
        """Use Kintsugi when we have had a Gold"""
        self.plr.coins.set(3)
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate", "Gold")
        self.plr.test_input = ["Trash Copper", "Get Estate"]
        self.plr.perform_event(self.card)
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])
        self.assertIn("Copper", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
