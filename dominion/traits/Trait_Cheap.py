#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Cheap"""
import unittest

from dominion import Card, Game, Trait, Player


###############################################################################
class Trait_Cheap(Trait.Trait):
    def __init__(self):
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "Cheap cards cost $1 less."
        self.name = "Cheap"

    def hook_card_cost(self, game: Game.Game, player: Player.Player, card: Card.Card) -> int:
        if card.pile in game.card_piles and game.card_piles[card.pile].trait == self.name:
            return -1
        return 0


###############################################################################
class Test_Cheap(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Cheap"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_cost(self) -> None:
        """Check cost of Cheap cards"""
        # Gold should never be cheaper as it shouldn't have a trait
        gold = self.g.get_card_from_pile("Gold")
        self.assertEqual(self.plr.card_cost(gold), 6)

        # Standard moat cost with no trait
        card = self.g.get_card_from_pile("Moat")
        self.g.assign_trait("Cheap", "Copper")  # Assign to non-moat
        self.g.card_piles["Moat"].trait = None
        self.assertEqual(self.plr.card_cost(card), 2)

        # Cheaper moat with the trait
        self.g.assign_trait("Cheap", "Moat")
        self.assertEqual(self.plr.card_cost(card), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
