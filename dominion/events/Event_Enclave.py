#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Enclave """

import unittest
from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Enclave(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Gain a Gold. Exile a Duchy from the Supply."
        self.name = "Enclave"
        self.cost = 8

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.gain_card("Gold")
        player.exile_card_from_supply("Duchy")


###############################################################################
class TestEnclave(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            events=["Enclave"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Enclave"]

    def test_enclave(self) -> None:
        """Use Enclave"""
        self.plr.coins.add(8)
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Gold"])
        self.assertIn("Duchy", self.plr.piles[Piles.EXILE])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
