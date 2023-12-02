#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sheepdog """

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_Sheepdog(Card.Card):
    """Sheepdog"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+2 Cards; When you gain a card, you may play this from your hand."
        self.name = "Sheepdog"
        self.cards = 2
        self.cost = 3

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if self in player.piles[Piles.HAND]:
            player.play_card(self, cost_action=False)
        return {}


###############################################################################
class TestSheepdog(unittest.TestCase):
    """Test Sheepdog"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Sheepdog"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sheepdog")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)

    def test_gain(self) -> None:
        """Gain a card"""
        self.plr.gain_card("Estate")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertIn("Sheepdog", self.plr.piles[Piles.PLAYED])

    def test_gain_twice(self) -> None:
        """Gain a card twice"""
        self.plr.gain_card("Estate")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.plr.gain_card("Estate")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
