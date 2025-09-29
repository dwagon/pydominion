#!/usr/bin/env python
"""Test Way"""

from dominion import Card, Way


###############################################################################
class Way_Test(Way.Way):
    """Test"""

    def __init__(self) -> None:
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.TEST
        self.desc = "Test"
        self.name = "Way of the Test"


# EOF
