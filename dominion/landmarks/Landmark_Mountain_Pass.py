#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Card, Game, Landmark, Player, OptionKeys


###############################################################################
class Landmark_MountainPass(Landmark.Landmark):
    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Mountain Pass"
        self._state = "un"

    def dynamic_description(self, player: Player.Player) -> str:
        if self._state == "done":
            return "Mountain Pass already claimed"
        return """When you are the first player to gain a Province, after that turn,
            each player bids once, up to 40 Debt, ending with you.
            High bidder gets +8VP and takes the Debt they bid."""

    def hook_end_turn(self, game: Game.Game, player: Player.Player) -> None:
        if self._state != "do":
            return
        plr = player
        curbid = 0
        winning_plr = None
        while True:
            plr = game.playerToRight(plr)
            opts = self.generate_bids(curbid)
            bid = plr.plr_choose_options("What to bid for 8VP?", *opts)
            if bid > curbid:
                curbid = bid
                winning_plr = plr
            if plr == player:
                break

        if winning_plr:
            winning_plr.debt += curbid
            winning_plr.add_score("Mountain Pass", 8)
            game.output("%s won with a bid of %d for 8VP" % (winning_plr.name, curbid))
            self._state = "done"
        else:
            game.output("No one bid for Mountain Pass")

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if self._state != "un":
            return {}
        if card.name == "Province":
            self._state = "do"
        return {}

    def generate_bids(self, minbid: int) -> list[tuple[str, int]]:
        options = [("Don't bid", -1)]
        for i in range(minbid + 1, 41):
            options.append((f"Bid {i}", i))
        return options


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return 0


###############################################################################
class TestMountainPass(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, landmarks=["Mountain Pass"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.mp = self.g.landmarks["Mountain Pass"]

    def test_play(self) -> None:
        """Test Mountain Pass"""
        self.assertEqual(self.mp._state, "un")
        self.plr.gain_card("Province")
        self.assertEqual(self.mp._state, "do")
        self.other.test_input = ["24"]
        self.plr.test_input = ["25"]
        self.plr.end_turn()
        self.assertEqual(self.plr.debt.get(), 25)
        self.assertEqual(self.other.debt.get(), 0)
        self.assertEqual(self.plr.get_score_details()["Mountain Pass"], 8)
        self.assertNotIn("Mountain Pass", self.other.get_score_details())
        self.assertEqual(self.mp._state, "done")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
