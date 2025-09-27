#!/usr/bin/env python
"""Test Trait"""

from dominion import Card, Trait


###############################################################################
class Trait_TestTrait(Trait.Trait):
    """Test Trait"""

    def __init__(self) -> None:
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.TEST
        self.desc = "Testing"
        self.name = "TestTrait"


# EOF
