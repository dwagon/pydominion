#!/usr/bin/env python

import unittest
from dominion import Game, Landmark


###############################################################################
class Landmark_Palace(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.desc = """When scoring, 3VP per set you have of Copper - Silver - Gold."""
        self.name = "Palace"

    def hook_end_of_game(self, game, player):
        num = {"Copper": 0, "Silver": 0, "Gold": 0}
        for card in player.all_cards():
            if card.name in num:
                num[card.name] += 1
        score = min(num.values()) * 3
        player.output(
            "Palace scored %d VP (%d Copper, %d Silver, %d Gold)"
            % (score, num["Copper"], num["Silver"], num["Gold"])
        )
        player.add_score("Palace", score)


###############################################################################
class Test_Palace(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, landmarkcards=["Palace"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Palace"""
        self.plr.set_discard("Gold", "Silver", "Silver", "Copper", "Duchy")
        self.plr.set_deck("Gold", "Silver", "Copper", "Copper", "Duchy")
        self.plr.set_hand("Silver", "Copper", "Copper", "Copper", "Duchy")
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Palace"], 2 * 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
