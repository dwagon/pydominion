#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Hasty"""
import unittest
from typing import Any

from dominion import Card, Game, Trait, Piles, PlayArea, Player, OptionKeys


###############################################################################
class Trait_Hasty(Trait.Trait):
    """Hasty"""

    def __init__(self) -> None:
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "When you gain a Hasty card, set it aside, and play it at the start of your next turn."
        self.name = "Hasty"
        self._aside = PlayArea.PlayArea("Hasty")

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        """When you gain a Hasty card, gain a Silver"""
        if game.card_piles[card.pile].trait == self.name:
            player.defer_card(card)
            return {OptionKeys.DONTADD: True}
        return {}


###############################################################################
class TestHasty(unittest.TestCase):
    """Test Hasty"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Hasty"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Check gaining Hasty cards"""
        self.g.assign_trait("Hasty", "Moat")
        self.plr.gain_card("Moat")
        self.plr.end_turn()
        self.plr.start_turn()
        self.g.print_state()
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
