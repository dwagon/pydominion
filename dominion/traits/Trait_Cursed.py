#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Cursed"""
import unittest
from typing import Any

from dominion import Card, Game, Trait, Piles, Player, OptionKeys, NoCardException


###############################################################################
class Trait_Cursed(Trait.Trait):
    """Cursed"""

    def __init__(self) -> None:
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "When you gain a Cursed card, gain a Loot and a Curse."
        self.name = "Cursed"
        self.required_cards = ["Loot", "Curse"]

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        """When you gain a Cursed card, +1 Buy."""
        if self.isTraitCard(game, card):
            try:
                player.gain_card("Curse")
            except NoCardException:
                player.output("No more Curses")
            try:
                player.gain_card("Loot")
            except NoCardException:
                player.output("No more Loot")
        return {}


###############################################################################
class Test_Cursed(unittest.TestCase):
    """Test Cursed"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Cursed"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_cost(self) -> None:
        """Check gaining Cursed cards"""
        self.g.assign_trait("Cursed", "Moat")
        buys = self.plr.buys.get()
        self.plr.gain_card("Moat")
        self.assertIn("Curse", self.plr.piles[Piles.DISCARD])

    def test_no_more_curses(self) -> None:
        """Check gaining a cursed card where there are no more curses"""
        self.g.assign_trait("Cursed", "Moat")
        while True:
            try:
                self.g.get_card_from_pile("Curse")
            except NoCardException:
                break
        self.plr.gain_card("Moat")
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Curse", self.plr.piles[Piles.DISCARD])

        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
