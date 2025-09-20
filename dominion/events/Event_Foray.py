#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Foray"""
import unittest

from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Foray(Event.Event):
    """Foray"""

    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Discard 3 cards, revealing them. If they have 3 different names, gain a Loot."""
        self.name = "Foray"
        self.cost = 3
        self.required_cards = ["Loot"]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        to_discard = player.plr_discard_cards(num=3)
        if not to_discard:
            return
        names: set[str] = set()
        for card in to_discard:
            player.reveal_card(card)
            names.add(card.name)
        if len(names) == 3:
            player.gain_card("Loot")


###############################################################################
class TestForay(unittest.TestCase):
    """Test Foray"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Foray"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Foray"]
        self.plr.coins.set(3)

    def test_no_discard(self) -> None:
        """Use Foray but don't discard anything"""
        self.plr.test_input = ["Finish"]
        self.plr.perform_event(self.event)
        found = any(True for _ in self.plr.piles[Piles.DISCARD] if _.isLoot())
        self.assertFalse(found)
        self.assertEqual(len(self.plr.piles[Piles.DISCARD]), 0)

    def test_diff_names(self) -> None:
        """Discard three different names"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.test_input = [
            "Discard Copper -",
            "Discard Silver -",
            "Discard Gold -",
            "Finish",
        ]
        self.plr.perform_event(self.event)
        found = any(True for _ in self.plr.piles[Piles.DISCARD] if _.isLoot())
        self.assertTrue(found)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
