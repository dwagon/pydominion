#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Scrounge"""
import unittest

from dominion import Card, Game, Event, Piles, Player


###############################################################################
class Event_Scrounge(Event.Event):
    """Scrounge"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Choose one: Trash a card from your hand; or gain an Estate from the trash,
        and if you did, gain a card costing up to $5."""
        self.name = "Scrounge"
        self.cost = 3

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        options = [
            ("Trash a card from your hand", True),
            ("Gain an Estate from the trash", False),
        ]
        if player.plr_choose_options("What to do with scrounge?", *options):
            player.plr_trash_card(num=1)
        elif estate := game.trash_pile["Estate"]:
            player.move_card(estate, Piles.DISCARD)
            player.plr_gain_card(5)


###############################################################################
class TestScrounge(unittest.TestCase):
    """Test Scrounge"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Scrounge"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Scrounge"]

    def test_play(self) -> None:
        """Perform a Scrounge and trash"""
        self.plr.coins.add(3)
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.test_input = ["Trash a card", "Trash Gold"]
        self.plr.perform_event(self.card)
        self.assertIn("Gold", self.g.trash_pile)

    def test_play_scrounge(self) -> None:
        """Perform a scrounge and pull an estate"""
        self.plr.coins.add(3)
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.g.trash_pile.set("Estate", "Gold")
        self.plr.test_input = ["Gain an Estate", "Get Silver -"]
        self.plr.perform_event(self.card)
        self.assertNotIn("Estate", self.g.trash_pile)
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
