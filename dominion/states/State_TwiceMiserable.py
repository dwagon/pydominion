#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, State


###############################################################################
class State_Twice_Miserable(State.State):
    def __init__(self):
        State.State.__init__(self)
        self.cardtype = Card.CardType.STATE
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "-4 VP"
        self.name = "Twice Miserable"
        self.victory = -4


###############################################################################
class Test_Twice_Miserable(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.state = self.g.states["Twice Miserable"]

    def test_have(self):
        self.plr.assign_state("Twice Miserable")
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Twice Miserable"], -4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
