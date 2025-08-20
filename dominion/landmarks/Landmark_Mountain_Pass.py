#!/usr/bin/env python

import unittest
from typing import Any, Optional

from dominion import Card, Game, Landmark, Player, OptionKeys


###############################################################################
class Landmark_MountainPass(Landmark.Landmark):
    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Mountain Pass"
        self.had_auction = False

    def dynamic_description(self, player: Player.Player) -> str:
        if self.had_auction:
            return "Mountain Pass already claimed"
        return """When you are the first player to gain a Province,
            each player bids once, up to 40 Debt, ending with you.
            High bidder gets +8VP and takes the Debt they bid."""

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if card.name != "Province":
            return {}
        if self.had_auction:
            return {}
        plr = player
        curr_bid = 0
        winning_plr: Optional[Player.Player] = None
        while True:
            plr = game.playerToRight(plr)
            opts = generate_bids(curr_bid)
            bid = plr.plr_choose_options("What to bid for 8VP?", *opts)
            if bid > curr_bid:
                curr_bid = bid
                winning_plr = plr
            if plr == player:
                break

        if winning_plr:
            winning_plr.debt += curr_bid
            winning_plr.add_score("Mountain Pass", 8)
            game.output(f"{winning_plr} won with a bid of {curr_bid} for 8VP")
            self.had_auction = True
        else:
            game.output("No one bid for Mountain Pass")
        return {}


def generate_bids(minbid: int) -> list[tuple[str, int]]:
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
        self.assertFalse(self.mp.had_auction)  # type: ignore
        self.other.test_input = ["24"]
        self.plr.test_input = ["25"]
        self.plr.gain_card("Province")
        self.assertEqual(self.plr.debt.get(), 25)
        self.assertEqual(self.other.debt.get(), 0)
        self.assertEqual(self.plr.get_score_details()["Mountain Pass"], 8)
        self.assertNotIn("Mountain Pass", self.other.get_score_details())
        self.assertTrue(self.mp.had_auction)  # type: ignore


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
