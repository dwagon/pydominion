#!/usr/bin/env python

import unittest
from typing import Optional, Any

from dominion import Card, Game, Way, Piles, OptionKeys, Player


###############################################################################
class Way_Horse(Way.Way):
    """Way of the Horse"""

    def __init__(self) -> None:
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+2 Cards; +1 Action; Return this to its pile."
        self.name = "Way of the Horse"
        self.cards = 2
        self.actions = 1

    def special_way(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> Optional[dict[OptionKeys, Any]]:
        player.move_card(card, Piles.CARDPILE)
        return {OptionKeys.DISCARD: False}


###############################################################################
class TestHorse(unittest.TestCase):
    """Test Way of the Horse"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            ways=["Way of the Horse"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Horse"]

    def test_play(self) -> None:
        """Perform a Horse"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertEqual(len(self.g.card_piles["Moat"]), 10)
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])
        self.assertNotIn("Moat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
