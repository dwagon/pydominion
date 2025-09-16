#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Reckless"""
import unittest
from typing import Any

from dominion import Card, Game, Trait, Player, Piles, OptionKeys


###############################################################################
class Trait_Reckless(Trait.Trait):
    def __init__(self):
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Follow the instructions of played Reckless cards twice.
                        When discarding one from play, return it to its pile."""
        self.name = "Reckless"

    def hook_post_play(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, str]:
        """Follow the instructions of played Reckless cards twice."""
        if self.isTraitCard(game, card):
            player.output(f"Playing {card} again")
            player.card_benefits(card)
        return {}

    def hook_discard_any_card(
        self, game: "Game.Game", player: "Player.Player", card: "Card.Card"
    ) -> dict[OptionKeys, Any]:
        """When discarding one from play, return it to its pile."""
        if self.isTraitCard(game, card):
            if card.location not in (Piles.TRASH, Piles.CARDPILE):
                player.output(f"Returning {card} to its pile")
                player.move_card(card, Piles.CARDPILE)
        return {}


###############################################################################
class Test_Reckless(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Reckless"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.assign_trait("Reckless", "Moat")

    def test_play(self) -> None:
        """Play Reckless card"""
        num_moats = len(self.g.card_piles["Moat"])
        self.plr.piles[Piles.HAND].empty()
        moat = self.plr.gain_card("Moat", Piles.HAND)
        self.plr.move_card(moat, Piles.HAND)
        self.plr.play_card(moat)
        self.assertEqual(len(self.g.card_piles["Moat"]), num_moats)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 4)  # Moat twice


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
