#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Fated"""
import unittest

from dominion import Card, Game, Trait, Player, PlayArea, Piles

FATED = "fated"


###############################################################################
class Trait_Fated(Trait.Trait):
    """Fated"""

    def __init__(self):
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """When shuffling, you may look through the cards and reveal Fated cards to
            put them on the top or bottom."""
        self.name = "Fated"

    def hook_pre_shuffle(self, game: "Game.Game", player: "Player.Player") -> None:
        """Reveal Fated cards"""
        if FATED not in player.specials:
            player.specials[FATED] = PlayArea.PlayArea("fated", initial=[])
        for card in player.piles[Piles.DISCARD]:
            if self.isTraitCard(game, card):
                player.specials[FATED].add(card)
                player.secret_count += 1

    def hook_post_shuffle(self, game: "Game.Game", player: "Player.Player") -> None:
        for card in player.specials.get(FATED, []):
            player.secret_count -= 1
            if player.plr_choose_options(f"Put {card} at top or bottom of deck?", ("Top", True), ("Bottom", False)):
                player.move_card(card, Piles.TOPDECK)
            else:
                player.move_card(card, Piles.DECK)
        player.specials[FATED] = PlayArea.PlayArea("fated", initial=[])


###############################################################################
class Test_Fated(unittest.TestCase):
    """Test Fated"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Fated"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.assign_trait("Fated", "Moat")

    def test_play_top(self) -> None:
        """Check Fated cards put on top"""
        self.plr.piles[Piles.DISCARD].set("Silver", "Silver", "Silver", "Silver", "Silver", "Moat")
        self.plr.piles[Piles.DECK].set()
        self.plr.test_input = ["Top"]
        self.plr.end_turn()
        self.assertIn("Moat", self.plr.piles[Piles.HAND])

    def test_play_bottom(self) -> None:
        """Check Fated cards put on bottom"""
        self.plr.piles[Piles.DISCARD].set("Silver", "Silver", "Silver", "Silver", "Silver", "Moat")
        self.plr.piles[Piles.DECK].set()
        self.plr.test_input = ["Bottom"]
        self.plr.end_turn()
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])
        self.assertIn("Moat", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
