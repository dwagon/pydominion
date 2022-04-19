#!/usr/bin/env python
""" Noop to make testing easier """

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_Noop(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = """ Nothing"""
        self.name = "noop"


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
