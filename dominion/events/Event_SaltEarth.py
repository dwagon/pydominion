#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Salt_the_Earth"""
import unittest
from dominion import Card, Game, Player, Event


###############################################################################
class Event_SaltEarth(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "+1VP. Trash a Victory card from the Supply."
        self.name = "Salt the Earth"
        self.cost = 4

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        player.add_score("Salt the Earth", 1)
        stacks = game.get_victory_piles()
        options: list[tuple[str, str | None]] = [("Select nothing", None)]
        options.extend((f"Select {stack}", stack) for stack in game.get_victory_piles())
        pile = player.plr_choose_options(
            "Trash a Victory card from the Supply", *options
        )
        if not pile:
            return
        card = game.get_card_from_pile(pile)
        player.trash_card(card)


###############################################################################
class Test_SaltEarth(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Salt the Earth"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Salt the Earth"]

    def test_event(self) -> None:
        """Use Salt the Earth"""
        self.plr.coins.add(4)
        self.plr.test_input = ["Province"]
        self.plr.perform_event(self.event)
        self.assertEqual(self.plr.get_score_details()["Salt the Earth"], 1)
        self.assertIn("Province", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
