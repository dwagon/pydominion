#!/usr/bin/env python
""" Noop to make testing easier """

from dominion import Card, Ally


###############################################################################
class Ally_Noop(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """ Nothing"""
        self.name = "noop"


# EOF
