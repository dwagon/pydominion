#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, State


###############################################################################
class State_Miserable(State.State):
    def __init__(self):
        State.State.__init__(self)
        self.cardtype = Card.CardType.STATE
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "-2 VP"
        self.name = "Miserable"
        self.victory = -2


###############################################################################
class Test_Miserable(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.state = self.g.states["Miserable"]

    def test_have(self):
        self.plr.assign_state("Miserable")
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Miserable"], -2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
