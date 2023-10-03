#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Fawning"""
import unittest
from dominion import Card, Game, Piles, Trait


###############################################################################
class Trait_Fawning(Trait.Trait):
    """Fawning"""

    def __init__(self):
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "When you gain a Province, gain a Fawning card."
        self.name = "Fawning"

    def hook_gain_card(self, game, player, card):
        """When you gain a province get something extra"""
        if card.name == "Province":
            player.gain_card(self.card_pile)


###############################################################################
class Test_Fawning(unittest.TestCase):
    """Test Fawning"""

    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=1, traits=["Fawning"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_cost(self):
        """Check gaining Fawning cards"""
        self.g.assign_trait("Fawning", "Moat")

        card = self.plr.gain_card("Province")
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
