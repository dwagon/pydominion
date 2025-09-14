#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Patient"""
import unittest
from typing import Any

from dominion import Card, Game, Trait, Player, Piles, PlayArea, OptionKeys

PATIENT = "patient"


###############################################################################
class Trait_Patient(Trait.Trait):
    def __init__(self) -> None:
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """At the start of your Clean-up phase, you may set aside Patient cards from your hand
            to play them at the start of your next turn."""
        self.name = "Patient"

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        if PATIENT not in player.specials:
            player.specials[PATIENT] = PlayArea.PlayArea(initial=[])
        for card in player.piles[Piles.HAND]:
            if not self.isTraitCard(game, card):
                continue
            if player.plr_choose_options(
                f"Set aside {card} to play next turn?", ("Do nothing", False), (f"Set aside {card}", True)
            ):
                player.output(f"Setting aside {card}")
                player.move_card(card, player.specials[PATIENT])
                player.secret_count += 1
        return {}

    def hook_start_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if PATIENT in player.specials:
            for card in player.specials[PATIENT]:
                player.output(f"Playing {card} from Patient")
                player.play_card(card, cost_action=False)
                player.secret_count -= 1
        player.specials[PATIENT] = PlayArea.PlayArea(initial=[])

    def debug_dump(self, player: Player.Player) -> None:
        if PATIENT in player.specials:
            player.output(f"Patient Reserve: {self}: {player.specials[PATIENT]}")


###############################################################################
class TestPatient(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Patient"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Play a patient card"""
        self.g.assign_trait("Patient", "Moat")
        self.plr.piles[Piles.HAND].set("Moat", "Copper", "Silver")
        self.plr.test_input = ["Set aside"]
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5 + 2)

    def test_no_play(self) -> None:
        """Play a patient card and don't set aside card"""
        self.g.assign_trait("Patient", "Moat")
        self.plr.piles[Piles.HAND].set("Moat", "Copper", "Silver")
        self.plr.test_input = ["Do nothing"]
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertNotIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
