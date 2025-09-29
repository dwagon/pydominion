#!/usr/bin/env python
"""Test Artifact"""

from dominion import Artifact, Card


###############################################################################
class Artifact_Test(Artifact.Artifact):
    """Test"""

    def __init__(self):
        Artifact.Artifact.__init__(self)
        self.base = Card.CardExpansion.TEST
        self.desc = "Test Artifact"
        self.name = "Test"


# EOF
