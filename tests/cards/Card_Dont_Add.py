#!/usr/bin/env python
""" Test the DONTADD function for gain card"""
from typing import Optional, Any
from dominion import Card, Game, Player, OptionKeys


###############################################################################
class Card_Dont_Add(Card.Card):
    """Test the DONTADD feature"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.name = "Don't Add"
        self.base = Card.CardExpansion.TEST

    def hook_gain_this_card(
        self,
        game: Game.Game,
        player: Player.Player,
    ) -> Optional[dict[OptionKeys, Any]]:
        """Dont add on gain"""
        return {OptionKeys.DONTADD: True}


# EOF
