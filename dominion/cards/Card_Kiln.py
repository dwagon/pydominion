#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Kiln """

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, NoCardException, OptionKeys


###############################################################################
class Card_Kiln(Card.Card):
    """Kiln"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+$2; The next time you play a card this turn, you may first gain a copy of it."""
        self.name = "Kiln"
        self.coin = 2
        self.cost = 5

    def hook_pre_play(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:  # pylint: disable=unused-argument
        """The next time you play a card this turn, you may first gain a copy of it."""
        if player.plr_choose_options(
            f"Gain a copy of {card}?",
            ("Do nothing", False),
            (f"Gain {card}", True),
        ):
            try:
                player.gain_card(card.name)
            except NoCardException:
                pass
        return {}


###############################################################################
class TestKiln(unittest.TestCase):
    """Test Kiln"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Kiln", "Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Kiln")
        self.village = self.g.get_card_from_pile("Village")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.add_card(self.village, Piles.HAND)

    def test_play(self) -> None:
        """Test play and gain card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.plr.actions.set(1)
        self.plr.test_input = ["Gain"]
        self.plr.play_card(self.village)
        self.assertIn("Village", self.plr.piles[Piles.DISCARD])
        self.assertIn("Village", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
