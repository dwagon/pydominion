#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Cursed"""
import unittest
from dominion import Card, Game, Trait, Piles


###############################################################################
class Trait_Cursed(Trait.Trait):
    """Cursed"""

    def __init__(self):
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = " When you gain a Cursed card, gain a Loot and a Curse."
        self.name = "Cursed"
        self.required_cards = ["Loot", "Curse"]

    def hook_gain_card(self, game, player, card):
        """When you gain a Cursed card, +1 Buy."""
        if game.card_piles[card.pile].trait == self.name:
            player.gain_card("Curse")
            player.gain_card("Loot")


###############################################################################
class Test_Cursed(unittest.TestCase):
    """Test Cursed"""

    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=1, traits=["Cursed"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_cost(self):
        """Check gaining Cursed cards"""
        self.g.assign_trait("Cursed", "Moat")
        buys = self.plr.buys.get()
        self.plr.gain_card("Moat")
        self.assertIn("Curse", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
