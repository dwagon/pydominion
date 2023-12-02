#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Hovel """

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_Hovel(Card.Card):
    """Hovel"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.REACTION, Card.CardType.SHELTER]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = "When you gain a Victory card, you may trash this from your hand."
        self.name = "Hovel"
        self.cost = 1
        self.purchasable = False
        self.victory = 0
        self.pile = "Shelters"

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if not card.isVictory():
            return {}
        if to_trash := player.plr_choose_options(
            "Trash Hovel?", ("Trash it", True), ("Keep it", False)
        ):
            player.trash_card(self)
        return {}


###############################################################################
def botresponse(
    player, kind, args=None, kwargs=None
):  # pragma: no cover, pylint: disable=unused-argument
    """bot response"""
    return True


###############################################################################
class TestHovel(unittest.TestCase):
    """Test Hovel"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Shelters"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_trash(self) -> None:
        """Test Trashing"""
        hovel = self.g.card_instances["Hovel"]  # You can't draw a hovel so we cheat
        self.plr.piles[Piles.HAND].empty()
        self.plr.piles[Piles.HAND].add(hovel)
        self.plr.test_input = ["Trash it"]
        self.plr.gain_card("Province")
        self.assertIn("Hovel", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
