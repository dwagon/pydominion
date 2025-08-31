#!/usr/bin/env python

from dominion import Loot, Card


###############################################################################
class Loot_Tester(Loot.Loot):
    """Tester"""

    def __init__(self) -> None:
        Loot.Loot.__init__(self)
        self.cardtype = [Card.CardType.LOOT, Card.CardType.TREASURE]
        self.base = Card.CardExpansion.TEST
        self.desc = "$3"
        self.name = "Tester"
        self.purchasable = False
        self.coin = 3
        self.cost = 7
        self.pile = "Loot"


# EOF
