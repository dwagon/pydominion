#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Rich"""
import unittest
from typing import Any

from dominion import Card, Game, Trait, Piles, Player, OptionKeys


###############################################################################
class Trait_Rich(Trait.Trait):
    """Rich"""

    def __init__(self) -> None:
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "When you gain a Rich card, gain a Silver."
        self.name = "Rich"

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        """When you gain a Rich card, gain a Silver"""
        if game.card_piles[card.pile].trait == self.name:
            player.gain_card("Silver")
        return {}


###############################################################################
class Test_Rich(unittest.TestCase):
    """Test Rich"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Rich"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_cost(self) -> None:
        """Check gaining Rich cards"""
        self.g.assign_trait("Rich", "Moat")
        buys = self.plr.buys.get()
        self.plr.gain_card("Moat")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
