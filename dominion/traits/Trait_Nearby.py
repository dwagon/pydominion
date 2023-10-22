#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Nearby"""
import unittest
from dominion import Card, Game, Piles, Trait


###############################################################################
class Trait_Nearby(Trait.Trait):
    """Nearby"""

    def __init__(self):
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "When you gain a Nearby card, +1 Buy."
        self.name = "Nearby"

    def hook_gain_card(self, game, player, card):
        """When you gain a Nearby card, +1 Buy."""
        if game.card_piles[card.pile].trait == self.name:
            player.buys.add(1)


###############################################################################
class Test_Nearby(unittest.TestCase):
    """Test Nearby"""

    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=1, traits=["Nearby"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_cost(self):
        """Check gaining Nearby cards"""
        self.g.assign_trait("Nearby", "Moat")
        buys = self.plr.buys.get()
        self.plr.gain_card("Moat")
        self.assertEqual(self.plr.buys.get(), buys + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
