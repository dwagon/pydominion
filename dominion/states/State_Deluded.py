#!/usr/bin/env python

import unittest
from dominion import Card, Game, State


###############################################################################
class State_Deluded(State.State):
    def __init__(self):
        State.State.__init__(self)
        self.cardtype = Card.TYPE_STATE
        self.base = Game.NOCTURNE
        self.desc = "At the start of your Buy phase, return this, and you can't buy Actions this turn."
        self.name = "Deluded"

    def hook_pre_buy(self, game, player):
        player.remove_state(self)

    def hook_card_cost(self, game, player, card):
        # Make action cards impossible to afford
        if card.isAction():
            return 99999
        return 0


###############################################################################
class Test_Deluded(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.state = self.g.states["Deluded"]

    def test_deluded(self):
        self.plr.assign_state("Deluded")
        self.plr.test_input = ["Estate"]
        self.assertGreater(self.plr.card_cost(self.g["Bard"]), 99)
        self.plr.test_input = ["End Phase"]
        self.plr.buy_phase()
        self.assertEqual(self.plr.states, [])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
