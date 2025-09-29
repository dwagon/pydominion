#!/usr/bin/env python
"""Test Prophecy"""

from dominion import Card, Prophecy


###############################################################################
class Prophecy_Test(Prophecy.Prophecy):
    "Test"

    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.TEST
        self.desc = "Test"
        self.name = "Test"


# EOF
