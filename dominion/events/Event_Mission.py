#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Mission"""
import unittest

from dominion import Card, Game, Event, Limits


###############################################################################
class Event_Mission(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """Once per turn: If the previous turn wasn't yours, take another turn after this one,
        during which you can't buy cards."""
        self.name = "Mission"
        self.cost = 4

    def special(self, game, player):
        if not game.last_turn(player):
            player.output("You had the previous turn")
            return

    def hook_end_turn(self, game, player):
        if game.last_turn(player):
            game.current_player = game.playerToRight(player)
            player.limits[Limits.BUY] = 0


###############################################################################
class TestMission(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2,
            events=["Mission"],
        )
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g.events["Mission"]

    def test_Mission(self):
        """Use Mission"""
        self.plr.coins.add(4)
        self.plr.perform_event(self.card)
        self.plr.end_turn()
        self.g.print_state()
        # TODO - need to test somehow


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
