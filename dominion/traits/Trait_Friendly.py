#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Friendly"""
import unittest

from dominion import Card, Game, Trait, Piles, Player, NoCardException


###############################################################################
class Trait_Friendly(Trait.Trait):
    """Friendly"""

    def __init__(self) -> None:
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "At the start of your Clean-up phase, you may discard a Friendly card to gain a Friendly card."
        self.name = "Friendly"

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> None:
        for card in player.piles[Piles.HAND]:
            if self.isTraitCard(game, card):
                if player.plr_choose_options(
                    f"Friendly Trait lets you to gain another {card}.", ("Do nothing", False), (f"Gain a {card}", True)
                ):
                    try:
                        player.gain_card(card.name)
                    except NoCardException:  # pragma: no coverage
                        player.output(f"No more {card}")
                break


###############################################################################
class Test_Friendly(unittest.TestCase):
    """Test Friendly"""

    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Friendly"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Check discarding Friendly cards"""
        self.g.assign_trait("Friendly", "Moat")
        self.plr.gain_card("Moat", Piles.HAND)
        self.plr.test_input = ["Gain a Moat"]
        self.plr.end_turn()
        self.assertEqual(self.plr.piles[Piles.DISCARD].count("Moat"), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
