#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Avanto"""
import unittest
from typing import Optional, Any

from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Avanto(Card.Card):
    """Avanto"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROMO
        self.desc = """+3 Cards; You may play a Sauna from your hand."""
        self.name = "Avanto"
        self.cost = 5
        self.cards = 3
        self.numcards = 5
        self.pile = "Sauna"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may play a Sauna from your hand."""
        if sauna := player.piles[Piles.HAND]["Sauna"]:
            if player.plr_choose_options(
                "Play an Sauna from your hand",
                ("Play Sauna", True),
                ("Don't play", False),
            ):
                player.play_card(sauna, cost_action=False)


###############################################################################
class TestAvanto(unittest.TestCase):
    """Test Avanto"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Sauna"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sauna", "Avanto")

    def test_play(self) -> None:
        """Play an Avanto"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate", "Sauna")
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Play Sauna"]
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertEqual(
            len(self.plr.piles[Piles.HAND]), hand_size + 1 + 3 - 1
        )  # +1 for Sauna, +3 for Avanto, -1 for playing Avanto
        self.assertIn("Sauna", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
