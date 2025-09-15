#!/usr/bin/env python
"""Test for card descriptions"""

from dominion import Card, Player, Game


###############################################################################
class Card_Description(Card.Card):
    """Test the descriptions"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.name = "Description"
        self.base = Card.CardExpansion.TEST

    def dynamic_description(self, player: "Player.Player") -> str:
        return "Foo"

    def hook_card_description(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> str:
        return "Bar"


# EOF
