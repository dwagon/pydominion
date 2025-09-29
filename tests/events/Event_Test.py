#!/usr/bin/env python
"""Test Event"""

from dominion import Card, Event


###############################################################################
class Event_Test(Event.Event):
    """Test Event"""

    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.TEST
        self.desc = "Test Event"
        self.name = "Test"
        self.cost = 0


# EOF
