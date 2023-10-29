#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Populate(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Gain one card from each Action Supply pile."
        self.name = "Populate"
        self.cost = 10

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        for card_name, card_pile in game.get_card_piles():
            card = game.card_instances[card_name]
            if not card:
                continue
            if card.isAction() and card.insupply:
                player.output(f"Gained {card_name} from Populate")
                player.gain_card(card_name)


###############################################################################
class TestPopulate(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            events=["Populate"],
            initcards=[
                "Cellar",
                "Chapel",
                "Moat",
                "Militia",
                "Village",
                "Workshop",
                "Gardens",
                "Mine",
                "Library",
                "Lurker",
            ],
            badcards=["Hostelry", "Border Village", "Inn"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Populate"]

    def test_Populate(self) -> None:
        """Use Populate"""
        self.plr.coins.add(10)
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Moat"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
