#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Journey"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Event, OptionKeys, Player, Phase


###############################################################################
class Event_Journey(Event.Event):
    """Journey"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """You don't discard cards from play in Clean-up this turn.
        Take an extra turn after this one (but not a 3rd turn in a row)."""
        self.name = "Journey"
        self.cost = 4

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        return {OptionKeys.DISCARD_PLAYED: False}

    def hook_end_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if not game.last_turn(player):
            game.current_player = game.playerToRight(player)


###############################################################################
class Test_Journey(unittest.TestCase):
    """Test Journey"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Journey"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Journey"]

    def test_play(self):
        """Perform a Journey"""
        self.plr.coins.add(4)
        self.plr.piles[Piles.PLAYED].set("Silver", "Gold")
        self.plr.perform_event(self.card)
        self.plr.end_turn()
        self.assertIn("Gold", self.plr.piles[Piles.PLAYED])
        self.plr.start_turn()
        self.g.print_state()
        self.assertEqual(self.plr.phase, Phase.START)
        self.assertIn("Gold", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
