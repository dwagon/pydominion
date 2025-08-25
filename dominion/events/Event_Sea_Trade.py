#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Sea_Trade"""
import unittest

from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Sea_Trade(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "+1 Card per Action card you have in play. Trash up to that many cards from your hand."
        self.name = "Sea Trade"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """+1 Card per Action card you have in play. Trash up to that many cards from your hand."""
        num_actions = sum(1 for _ in player.piles[Piles.PLAYED] if _.isAction())
        if num_actions == 0:
            player.output("No actions played")
            return
        player.pickup_cards(num=num_actions)
        player.plr_trash_card(num=num_actions)


###############################################################################
class TestSea_Trade(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            events=["Sea Trade"],
            initcards=["Moat"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Sea Trade"]

    def test_play(self) -> None:
        """No actions in play"""
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Province")
        self.plr.piles[Piles.PLAYED].set("Moat", "Moat")
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.coins.set(4)
        self.plr.test_input = ["Trash Estate", "Trash Copper", "Finish"]
        self.plr.perform_event(self.card)
        self.assertIn("Estate", self.g.trash_pile)
        self.assertEqual(len(self.g.trash_pile), 2)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size - 2 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
