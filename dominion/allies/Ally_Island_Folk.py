#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Island_Folk"""

import unittest

from dominion import Card, Game, Ally, Player, Phase


###############################################################################
class Ally_Island_Folk(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """At the end of your turn, you may spend 5 Favors to take an extra turn after
        this one (but not a 3rd turn in a row)."""
        self.name = "Island Folk"

    def hook_end_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if player.favors.get() < 5:
            return
        if game.last_turn(player):
            return
        if player.plr_choose_options(
            "Spend 5 favors to take an extra turn? ",
            ("Do nothing", False),
            (f"Spend 5 favors)", True),
        ):
            player.output("Having an extra turn")
            player.favors.add(-5)
            game.current_player = game.playerToRight(player)


###############################################################################
class Test_Island_Folk(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, allies="Island Folk", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        self.plr.favors.set(5)
        self.plr.test_input = ["Spend 5"]
        self.plr.phase = Phase.BUY
        self.plr.end_turn()
        self.assertEqual(self.plr.favors.get(), 0)
        self.assertEqual(self.plr.phase, Phase.NONE)
        # Not a great test


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
