#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Alliance(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = (
            "Gain a Province, a Duchy, an Estate, a Gold, a Silver, and a Copper."
        )
        self.name = "Alliance"
        self.cost = 10

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.gain_card("Province")
        player.gain_card("Duchy")
        player.gain_card("Estate")
        player.gain_card("Gold")
        player.gain_card("Silver")
        player.gain_card("Copper")


###############################################################################
class TestAlliance(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Alliance"], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Alliance"]

    def test_play(self) -> None:
        """Perform an Alliance"""
        self.plr.coins.add(10)
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Province"])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Gold"])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Copper"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
