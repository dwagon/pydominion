#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Rich"""
import unittest
from dominion import Card, Game, Trait, Piles


###############################################################################
class Trait_Rich(Trait.Trait):
    """Rich"""

    def __init__(self):
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "When you gain a Rich card, gain a Silver."
        self.name = "Rich"

    def hook_gain_card(self, game, player, card):
        """When you gain a Rich card, gain a Silver"""
        if game.card_piles[card.pile].trait == self.name:
            player.gain_card("Silver")


###############################################################################
class Test_Rich(unittest.TestCase):
    """Test Rich"""

    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=1, traits=["Rich"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_cost(self):
        """Check gaining Rich cards"""
        self.g.assign_trait("Rich", "Moat")
        buys = self.plr.buys.get()
        self.plr.gain_card("Moat")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
