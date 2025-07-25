#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Landmark


###############################################################################
class Landmark_Arena(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Arena"

    def dynamic_description(self, player):
        return (
            "At the start of your Buy phase, you may discard an Action card. If you do, take 2VP from here. (%d left)"
            % self._vp
        )

    def setup(self, game):
        self._vp = 6 * game.numplayers

    def hook_pre_buy(self, game, player):
        if self._vp <= 0:
            return
        actions = []
        for card in player.piles[Piles.HAND]:
            if card.isAction():
                actions.append(card)
        if not actions:
            return
        disc = player.plr_discard_cards(prompt="Arena: Discard an action to gain 2VP", cardsrc=actions)
        if disc:
            player.output("Gained 2 VP from Arena")
            self._vp -= 2
            player.add_score("Arena", 2)


###############################################################################
class Test_Arena(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, landmarks=["Arena"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Arena"""
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.test_input = ["Discard Moat", "End Phase"]
        self.plr.buy_phase()
        self.assertEqual(self.plr.get_score_details()["Arena"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
