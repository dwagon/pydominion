#!/usr/bin/env python

import unittest
from dominion import Game, Landmark


###############################################################################
class Landmark_DefiledShrine(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.desc = "When you gain an Action, move 1VP from its pile to this. When you buy a Curse, take the VP from this."
        self.name = "Defiled Shrine"
        self.required_cards = ["Curse"]
        self.stored_vp = 0

    @classmethod
    def setup(cls, game):
        cls._vp = {}
        for cp in list(game.cardpiles.values()):
            if not cp.isGathering():
                cls._vp[cp.name] = 2

    def hook_all_players_buy_card(self, game, player, owner, card):
        if game.landmarks["Defiled Shrine"]._vp[card.name]:
            game.landmarks["Defiled Shrine"]._vp[card.name] -= 1
            self.stored_vp += 1

    def hook_buy_card(self, game, player, card):
        if card.name == "Curse":
            player.add_score("Defiled Shrine", self.stored_vp)
            self.stored_vp = 0


###############################################################################
class Test_DefiledShrine(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=2,
            landmarkcards=["Defiled Shrine"],
            initcards=["Moat"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_use(self):
        """Use Defiled Shrine"""
        self.plr.set_buys(2)
        self.plr.set_coins(5)
        self.assertEqual(self.g.landmarks["Defiled Shrine"]._vp["Moat"], 2)
        self.plr.buy_card(self.g["Moat"])
        self.assertEqual(self.g.landmarks["Defiled Shrine"]._vp["Moat"], 1)
        self.plr.buy_card(self.g["Curse"])
        self.assertEqual(self.plr.score["Defiled Shrine"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
