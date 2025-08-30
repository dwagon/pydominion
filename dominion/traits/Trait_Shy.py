#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Shy"""
import unittest

from dominion import Card, Game, Trait, Player, Piles


###############################################################################
class Trait_Shy(Trait.Trait):
    def __init__(self) -> None:
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "At the start of your turn, you may discard one Shy card for +2 Cards."
        self.name = "Shy"

    def hook_start_turn(self, game: Game.Game, player: Player.Player) -> None:
        if self.card_pile not in player.piles[Piles.HAND]:
            return
        assert self.card_pile is not None
        shy_card = player.piles[Piles.HAND][self.card_pile]
        desc = game.card_instances[self.card_pile].description(player)
        if player.plr_choose_options(
            f"Discard a {self.card_pile} ({desc}) to pickup two cards",
            (f"Discard {self.card_pile}", True),
            ("Keep Card", False),
        ):
            player.discard_card(shy_card)
            player.pickup_cards(2)


###############################################################################
class TestShy(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Shy"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Check cost of Shy cards"""
        self.g.assign_trait("Shy", "Moat")
        self.plr.piles[Piles.HAND].set("Moat", "Copper", "Silver", "Moat")
        self.plr.test_input = ["Discard"]
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertIn("Moat", self.plr.piles[Piles.HAND])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 4 + 2 - 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
