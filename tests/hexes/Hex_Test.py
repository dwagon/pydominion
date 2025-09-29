#!/usr/bin/env python
"""Test Hex"""
from dominion import Card, Hex


###############################################################################
class Hex_Test(Hex.Hex):
    """Test"""

    def __init__(self):
        Hex.Hex.__init__(self)
        self.cardtype = Card.CardType.HEX
        self.base = Card.CardExpansion.TEST
        self.desc = "Test"
        self.name = "Test Hex"
        self.purchasable = False


# EOF
