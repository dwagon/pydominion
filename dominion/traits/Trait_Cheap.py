#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Cheap"""
import unittest
from dominion import Card, Game, Piles, Trait


###############################################################################
class Trait_Cheap(Trait.Trait):
    def __init__(self):
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "Cheap cards cost $1 less."
        self.name = "Cheap"

    def hook_card_cost(self, game, player, card):
        return -1


###############################################################################
class Test_Cheap(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            quiet=True, numplayers=1, traits=["Cheap"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_cost(self):
        """Check cost of Cheap cards"""
        card = self.g.get_card_from_pile("Moat")
        self.g.card_piles["Moat"].trait = None
        self.assertEqual(self.plr.card_cost(card), 2)
        self.g.card_piles["Moat"].trait = self.g.traits["Cheap"]
        self.assertEqual(self.plr.card_cost(card), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF