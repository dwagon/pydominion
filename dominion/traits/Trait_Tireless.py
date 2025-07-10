#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Tireless"""
import unittest
from typing import Any

from dominion import Card, Game, Trait, Piles, Player, OptionKeys, PlayArea


###############################################################################
class Trait_Tireless(Trait.Trait):
    """Tireless"""

    def __init__(self) -> None:
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = (
            "When you discard a Tireless card from play, set it aside, and put it onto your deck at end of turn."
        )
        self.name = "Tireless"
        self.set_aside = PlayArea.PlayArea()

    def hook_discard_any_card(
        self, game: "Game.Game", player: "Player.Player", card: "Card.Card"
    ) -> dict[OptionKeys, Any]:
        if game.card_piles[card.pile].trait == self.name:
            player.move_card(card, self.set_aside)
            player.secret_count += 1
            player.output(f"Setting Tireless {card} aside")
        return {}

    def hook_end_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if self.set_aside:
            card = self.set_aside.next_card()
            player.output(f"Putting {card} back in hand from Tireless")
            player.add_card(card, Piles.HAND)
            player.secret_count -= 1


###############################################################################
class Test_Tireless(unittest.TestCase):
    """Test Tireless"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Tireless"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_cost(self) -> None:
        """Check gaining Tireless cards"""
        self.g.assign_trait("Tireless", "Moat")
        moat = self.g.get_card_from_pile("Moat")
        self.plr.move_card(moat, Piles.HAND)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.piles[Piles.HAND])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5 + 1)  # Hand + Moat


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
