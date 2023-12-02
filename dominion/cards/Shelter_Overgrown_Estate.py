#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Overgrown_Estate """

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_Overgrown_Estate(Card.Card):
    """Overgrown Estate"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.VICTORY, Card.CardType.SHELTER]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = "0VP; When you trash this, +1 Card."
        self.name = "Overgrown Estate"
        self.cost = 1
        self.victory = 0
        self.purchasable = False
        self.pile = "Shelters"

    def hook_trash_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, Any]:
        player.pickup_cards(1)
        return {}


###############################################################################
class TestOvergrownEstate(unittest.TestCase):
    """Test Overgrown Estate"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Shelters"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Test Play"""
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.piles[Piles.HAND].set("Overgrown Estate")
        card = self.plr.piles[Piles.HAND]["Overgrown Estate"]
        self.plr.trash_card(card)
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Overgrown Estate", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
