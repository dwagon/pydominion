#!/usr/bin/env python
"""Test dynamic card type"""
from dominion import Card
from dominion.Card import CardType


###############################################################################
class Card_DynaType(Card.Card):
    """Card with Dynamic Type"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.name = "Dyna Type"
        self.base = Card.CardExpansion.TEST

    def hook_add_dynamic_card_type(self, card: Card.Card) -> CardType:
        return Card.CardType.NIGHT


# EOF
