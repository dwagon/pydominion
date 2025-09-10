#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Pious"""
import unittest
from typing import Any

from dominion import Card, Game, Trait, Player, OptionKeys, Piles


###############################################################################
class Trait_Pious(Trait.Trait):
    def __init__(self):
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """When you gain a Pious card, you may trash a card from your hand."""
        self.name = "Pious"

    def hook_gain_card(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, Any]:
        if self.isTraitCard(game, card):
            player.plr_trash_card(1)
        return {}


###############################################################################
class Test_Pious(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Pious"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.assign_trait("Pious", "Moat")

    def test_play(self) -> None:
        """Play Pious card"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.test_input = ["Trash Copper"]
        self.plr.gain_card("Moat")
        self.assertIn("Copper", self.g.trash_pile)
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
